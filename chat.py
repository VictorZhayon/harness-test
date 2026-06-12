"""
api/routes/chat.py
──────────────────
POST /projects/{project_id}/chat/extraction/message  — send a message, get AI reply
POST /projects/{project_id}/chat/extraction/extract  — trigger task extraction
POST /tasks/{task_id}/chat/message                   — execution assistant message
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.exceptions import AIExtractionError, ProjectNotFoundError, TaskNotFoundError
from core.models import TaskStatus, User
from db.database import get_db
from db.repositories import ConversationRepository, ProjectRepository, TaskRepository
from services.extraction_service import extract_tasks
from services.execution_service import send_execution_message
from api.dependencies import get_current_user

router = APIRouter(tags=["Chat"])

# ---------------------------------------------------------------------------
# Extraction chat
# ---------------------------------------------------------------------------

class MessageRequest(BaseModel):
    content: str


class MessageResponse(BaseModel):
    role: str
    content: str
    session_id: str


@router.post(
    "/projects/{project_id}/chat/extraction/message",
    response_model=MessageResponse,
)
def extraction_chat_message(
    project_id: str,
    body: MessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a message in the extraction chat.
    The AI responds conversationally (not yet extracting tasks).
    """
    project = ProjectRepository(db).get_by_id(project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Project not found.")

    conv_repo = ConversationRepository(db)

    # Find or create extraction session for this project
    # (simplified: one extraction session per project)
    session = _get_or_create_extraction_session(conv_repo, project_id, current_user.id)

    # Persist user message
    conv_repo.append_message(session.id, "user", body.content)
    messages = conv_repo.get_messages(session.id)

    # Lightweight ack — in production you'd stream this
    ack = (
        "Got it. Keep describing your project, or say 'extract tasks' when ready."
    )
    conv_repo.append_message(session.id, "model", ack)

    return MessageResponse(role="model", content=ack, session_id=session.id)


@router.post(
    "/projects/{project_id}/chat/extraction/extract",
    status_code=status.HTTP_201_CREATED,
)
def trigger_extraction(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Run the full task extraction from the conversation history.
    Returns proposed tasks (PROPOSED status — not yet on canvas).
    """
    project = ProjectRepository(db).get_by_id(project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Project not found.")

    conv_repo = ConversationRepository(db)
    session = _get_or_create_extraction_session(conv_repo, project_id, current_user.id)
    messages = conv_repo.get_messages(session.id)

    if len(messages) < 2:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Tell Sio more about your project before extracting tasks.",
        )

    try:
        proposed_tasks = extract_tasks(project_id, messages)
    except AIExtractionError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

    task_repo = TaskRepository(db)
    saved = task_repo.bulk_create(proposed_tasks)

    return {
        "session_id": session.id,
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "why": t.why,
                "estimated_minutes": t.estimated_minutes,
                "status": t.status.value,
            }
            for t in saved
        ],
    }


# ---------------------------------------------------------------------------
# Execution chat
# ---------------------------------------------------------------------------

@router.post("/tasks/{task_id}/chat/message", response_model=MessageResponse)
def execution_chat_message(
    task_id: str,
    body: MessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a message to the per-task execution assistant.
    Only works for CONFIRMED tasks.
    """
    task_repo = TaskRepository(db)
    task = task_repo.get_by_id(task_id)

    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found.")
    if task.status != TaskStatus.CONFIRMED:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Only confirmed tasks have an execution assistant.",
        )

    conv_repo = ConversationRepository(db)
    session = _get_or_create_execution_session(
        conv_repo, task.project_id, current_user.id, task_id
    )

    conv_repo.append_message(session.id, "user", body.content)
    history = conv_repo.get_messages(session.id)

    reply = send_execution_message(task, history[:-1], body.content)
    conv_repo.append_message(session.id, "model", reply)

    return MessageResponse(role="model", content=reply, session_id=session.id)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_or_create_extraction_session(conv_repo, project_id, user_id):
    # In production, store session_id client-side and look it up by ID
    # For MVP: one extraction session per project (create if not exists)
    from db.database import SessionLocal
    from db.database import ConversationSessionORM
    db = conv_repo.db
    orm = (
        db.query(ConversationSessionORM)
        .filter_by(project_id=project_id, context_type="extraction")
        .first()
    )
    if orm:
        return conv_repo.get_session(orm.id)
    return conv_repo.create_session(project_id, user_id, "extraction")


def _get_or_create_execution_session(conv_repo, project_id, user_id, task_id):
    from db.database import ConversationSessionORM
    db = conv_repo.db
    orm = (
        db.query(ConversationSessionORM)
        .filter_by(task_id=task_id, context_type="execution")
        .first()
    )
    if orm:
        return conv_repo.get_session(orm.id)
    return conv_repo.create_session(project_id, user_id, "execution", task_id=task_id)
