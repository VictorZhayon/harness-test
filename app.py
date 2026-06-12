"""
Selah — Before you lead a choir, take a Selah.
MVP Streamlit Prototype v1.1 — Gemini Edition
All screens: Login, Upload, Analysis, Song Brief, Song Library
Intelligence layer: Google Gemini 1.5 Pro
"""

import streamlit as st
import json
import os
import time
from datetime import datetime

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Selah",
    page_icon="assets/favicon.png" if os.path.exists("assets/favicon.png") else "🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Selah design tokens ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,700;1,400;1,700&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --indigo:        #3730A3;
    --indigo-mid:    #4F46E5;
    --indigo-light:  #EDEBFF;
    --indigo-soft:   #C4BFFF;
    --ink:           #1A1209;
    --slate:         #5C4E3A;
    --muted:         #9E8E78;
    --white:         #FDFAF4;
    --off-white:     #F5F0E8;
    --rule:          #E8DFD0;
    --amber:         #B45309;
    --amber-light:   #FDF3DC;
    --sage:          #166534;
    --sage-light:    #DCFCE7;
    --error:         #B91C1C;
    --error-light:   #FEF2F2;
}

/* ── Global reset ─────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--off-white) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: var(--white) !important;
    border-right: 1px solid var(--rule) !important;
}
[data-testid="stSidebar"] * {
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Headings ─────────────────────────────────────────────── */
h1, h2 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--ink) !important;
}
h3, h4, label, p {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--ink) !important;
}

/* ── Primary button ───────────────────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button {
    background-color: var(--indigo) !important;
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0 24px !important;
    height: 40px !important;
    transition: background 100ms ease-out !important;
}
.stButton > button:hover {
    background-color: var(--indigo-mid) !important;
}

/* ── Cards ────────────────────────────────────────────────── */
.selah-card {
    background: var(--white);
    border: 1px solid var(--rule);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(26,18,9,0.06), 0 1px 2px rgba(26,18,9,0.04);
    margin-bottom: 16px;
}
.selah-card:hover {
    box-shadow: 0 4px 12px rgba(26,18,9,0.10);
    border-color: var(--indigo-soft);
}

/* ── Badges ───────────────────────────────────────────────── */
.badge-key, .badge-bpm {
    display: inline-block;
    background: var(--indigo);
    color: var(--white) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 20px;
    font-weight: 500;
    border-radius: 8px;
    padding: 8px 20px;
    margin-right: 12px;
}
.badge-section {
    display: inline-block;
    background: var(--indigo-light);
    color: var(--indigo) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-radius: 6px;
    padding: 3px 10px;
    margin-right: 6px;
    margin-bottom: 4px;
}
.badge-chord {
    display: inline-block;
    background: var(--off-white);
    border: 1px solid var(--rule);
    color: var(--ink) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px;
    border-radius: 6px;
    padding: 4px 10px;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* ── Song Brief header ────────────────────────────────────── */
.brief-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 36px !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
    line-height: 1.2 !important;
    margin-bottom: 4px !important;
}
.brief-subtitle {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: var(--slate) !important;
    margin-bottom: 24px !important;
}
.brief-section-heading {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 26px !important;
    font-weight: 500 !important;
    color: var(--ink) !important;
    border-bottom: 1px solid var(--rule) !important;
    padding-bottom: 8px !important;
    margin-top: 32px !important;
    margin-bottom: 16px !important;
}

/* ── Logo wordmark ────────────────────────────────────────── */
.selah-logo {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 600 !important;
    font-size: 28px !important;
    letter-spacing: 0.1em !important;
    color: var(--indigo) !important;
    text-transform: uppercase !important;
}
.selah-logo-lamed {
    font-size: 22px;
    margin-right: 6px;
    color: var(--indigo);
}

/* ── Status / info boxes ──────────────────────────────────── */
.status-processing {
    background: var(--amber-light);
    border-left: 4px solid var(--amber);
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
    margin: 16px 0;
}
.status-success {
    background: var(--sage-light);
    border-left: 4px solid var(--sage);
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
    margin: 16px 0;
}
.status-error {
    background: var(--error-light);
    border-left: 4px solid var(--error);
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
    margin: 16px 0;
}

/* ── Lyrics block ─────────────────────────────────────────── */
.lyrics-section {
    background: var(--white);
    border: 1px solid var(--rule);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
}
.lyrics-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--slate);
    margin-bottom: 8px;
}
.lyrics-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.75;
    color: var(--ink);
    white-space: pre-line;
}

/* ── Upload zone ──────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--white) !important;
    border: 2px dashed var(--rule) !important;
    border-radius: 12px !important;
    padding: 32px !important;
}

/* ── Chord timeline ───────────────────────────────────────── */
.chord-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid var(--rule);
}
.chord-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    min-width: 48px;
}
.chord-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    font-weight: 500;
    color: var(--ink);
    min-width: 60px;
}
.chord-numeral {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--slate);
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ───────────────────────────────────────────────────────
def init_state():
    defaults = {
        "authenticated": False,
        "user_email": "",
        "user_name": "",
        "current_screen": "login",  # login | dashboard | upload | analysis | brief
        "song_library": [],
        "current_brief": None,
        "analysis_error": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Imports for analysis (with graceful fallback) ────────────────────────────
try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
except ImportError:
    ASSEMBLYAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

# ── Analysis functions ───────────────────────────────────────────────────────

def analyse_with_librosa(audio_path: str) -> dict:
    """Run Librosa analysis: key, tempo, time signature, chords."""
    if not LIBROSA_AVAILABLE:
        raise RuntimeError("librosa is not installed. Run: pip install librosa")

    y, sr = librosa.load(audio_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    # ── Tempo & beat tracking
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()
    tempo_val = float(tempo) if not hasattr(tempo, '__len__') else float(tempo[0])

    # ── Key detection using chroma
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    dominant_pitch = pitch_classes[int(chroma_mean.argmax())]

    # Simple major/minor heuristic using chroma
    major_profile = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
    minor_profile = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
    major_corr = np.corrcoef(chroma_mean, major_profile)[0,1]
    minor_corr = np.corrcoef(chroma_mean, minor_profile)[0,1]
    mode = "Major" if major_corr >= minor_corr else "Minor"
    detected_key = f"{dominant_pitch} {mode}"

    # ── Time signature heuristic (3/4 vs 4/4 vs 6/8)
    # Use onset strength envelope autocorrelation
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    ac = librosa.autocorrelate(onset_env, max_size=sr // 2)
    # Rough heuristic: look at 3 vs 4 beat periodicity
    tempo_period = sr / tempo_val
    beat3 = ac[int(tempo_period * 3)] if int(tempo_period * 3) < len(ac) else 0
    beat4 = ac[int(tempo_period * 4)] if int(tempo_period * 4) < len(ac) else 0
    time_sig = "3/4" if beat3 > beat4 * 0.9 else "4/4"

    # ── Chord detection (simplified using chroma frames)
    hop_length = 512
    chroma_frames = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
    frame_times = librosa.frames_to_time(
        np.arange(chroma_frames.shape[1]), sr=sr, hop_length=hop_length
    )

    # Sample every ~4 seconds for chord changes
    sample_interval = int(4 * sr / hop_length)
    chord_timeline = []
    chord_map = {
        0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
        6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
    }
    for i in range(0, chroma_frames.shape[1], sample_interval):
        frame_chroma = chroma_frames[:, i]
        root = int(frame_chroma.argmax())
        # Simplified: if minor tendency (minor third 3 semitones up is strong)
        third_minor = (root + 3) % 12
        third_major = (root + 4) % 12
        is_minor = frame_chroma[third_minor] > frame_chroma[third_major]
        chord_name = chord_map[root] + ("m" if is_minor else "")
        timestamp = float(frame_times[i]) if i < len(frame_times) else 0.0
        chord_timeline.append({
            "time": round(timestamp, 1),
            "chord": chord_name,
            "time_label": f"{int(timestamp//60)}:{int(timestamp%60):02d}"
        })

    # Deduplicate consecutive same chords
    deduped = []
    for c in chord_timeline:
        if not deduped or deduped[-1]["chord"] != c["chord"]:
            deduped.append(c)

    return {
        "key": detected_key,
        "tempo_bpm": round(tempo_val, 1),
        "time_signature": time_sig,
        "duration_seconds": round(duration, 1),
        "beat_count": len(beat_times),
        "chord_timeline": deduped,
        "beat_times_sample": beat_times[:20],  # first 20 for display
    }


def transcribe_with_assemblyai(audio_path: str, api_key: str) -> dict:
    """Transcribe audio using AssemblyAI with speaker labels and chapters."""
    if not ASSEMBLYAI_AVAILABLE:
        raise RuntimeError("assemblyai is not installed. Run: pip install assemblyai")

    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(
        auto_chapters=True,
        speaker_labels=False,
        punctuate=True,
        format_text=True,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"AssemblyAI error: {transcript.error}")

    chapters = []
    if transcript.chapters:
        for ch in transcript.chapters:
            chapters.append({
                "start_ms": ch.start,
                "end_ms": ch.end,
                "summary": ch.summary,
                "headline": ch.headline,
                "gist": ch.gist,
            })

    return {
        "full_text": transcript.text or "",
        "chapters": chapters,
        "words": [
            {"text": w.text, "start_ms": w.start, "end_ms": w.end}
            for w in (transcript.words or [])
        ],
    }


def build_song_brief_with_gemini(
    song_title: str,
    librosa_data: dict,
    transcription_data: dict,
    api_key: str,
) -> dict:
    """Use Gemini 1.5 Pro to interpret raw analysis and structure the Song Brief."""
    if not GEMINI_AVAILABLE:
        raise RuntimeError("google-generativeai is not installed. Run: pip install google-generativeai")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=genai.GenerationConfig(
            temperature=0.2,          # Low temp for consistent structured output
            response_mime_type="application/json",  # Native JSON mode — no fencing needed
        ),
        system_instruction="""You are Selah's music intelligence layer. You receive raw audio analysis data
and produce a structured Song Brief for a gospel or worship music director.

You must respond with ONLY a valid JSON object matching this exact schema:
{
  "song_title": "string",
  "key": "string (e.g. G Major)",
  "tempo_bpm": number,
  "time_signature": "string",
  "duration": "string (e.g. 4:32)",
  "key_summary": "2-3 sentence summary of the song's musical character for a director",
  "chord_progression_summary": "plain English description of the main progression",
  "main_chords": ["list", "of", "chord", "names"],
  "roman_numeral_progression": "e.g. I - IV - V - I",
  "song_structure": [
    {"section": "Intro", "timing": "0:00 - 0:20", "notes": "brief description"}
  ],
  "lyrics_by_section": [
    {"section": "Verse 1", "lyrics": "full lyrics for this section"}
  ],
  "harmony_notes": "paragraph describing where harmonies occur and voice leading notes",
  "director_notes": "2-3 practical notes for leading this song with a choir",
  "repeat_structure": "plain English description of repeats and song flow"
}"""
    )

    prompt = f"""Song title: {song_title}

LIBROSA ANALYSIS:
{json.dumps(librosa_data, indent=2)}

ASSEMBLYAI TRANSCRIPTION:
Full text: {transcription_data.get('full_text', '')[:3000]}

Chapters/sections detected: {json.dumps(transcription_data.get('chapters', []), indent=2)}

Produce the complete Song Brief JSON."""

    response = model.generate_content(prompt)

    # response_mime_type="application/json" means .text is already clean JSON
    return json.loads(response.text)


# ── PDF export ───────────────────────────────────────────────────────────────

def generate_pdf(brief: dict) -> bytes:
    """Generate a printable Song Brief PDF."""
    if not FPDF_AVAILABLE:
        return None

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=18)

    # ── Header
    pdf.set_font("Helvetica", 'B', 24)
    pdf.set_text_color(55, 48, 163)
    pdf.cell(0, 12, "SELAH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 10)
    pdf.set_text_color(92, 78, 58)
    pdf.cell(0, 6, "Before you lead a choir, take a Selah.", ln=True, align='C')
    pdf.ln(4)
    pdf.set_draw_color(232, 223, 208)
    pdf.set_line_width(0.5)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(6)

    # ── Song title
    pdf.set_font("Helvetica", 'B', 20)
    pdf.set_text_color(26, 18, 9)
    pdf.cell(0, 10, brief.get("song_title", "Song Brief"), ln=True)
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(92, 78, 58)
    pdf.cell(0, 6, f"Generated {datetime.now().strftime('%d %B %Y')}", ln=True)
    pdf.ln(6)

    # ── Key stats row
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(26, 18, 9)
    stats = [
        ("KEY", brief.get("key", "—")),
        ("BPM", str(brief.get("tempo_bpm", "—"))),
        ("TIME SIG", brief.get("time_signature", "—")),
        ("DURATION", brief.get("duration", "—")),
    ]
    col_w = (pdf.w - 36) / 4
    for label, val in stats:
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.set_fill_color(237, 235, 255)
        pdf.rect(x, y, col_w - 4, 14, 'F')
        pdf.set_font("Helvetica", '', 8)
        pdf.set_text_color(92, 78, 58)
        pdf.set_xy(x + 3, y + 2)
        pdf.cell(col_w - 10, 4, label, ln=False)
        pdf.set_xy(x + 3, y + 7)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.set_text_color(55, 48, 163)
        pdf.cell(col_w - 10, 5, val, ln=False)
        pdf.set_xy(x + col_w, y)
    pdf.ln(20)

    def section_heading(title):
        pdf.set_font("Helvetica", 'B', 14)
        pdf.set_text_color(26, 18, 9)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_draw_color(232, 223, 208)
        pdf.line(18, pdf.get_y(), 192, pdf.get_y())
        pdf.ln(4)

    def body_text(text, color=(26, 18, 9)):
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(*color)
        pdf.multi_cell(0, 5, text)
        pdf.ln(2)

    # ── Key summary
    section_heading("Overview")
    body_text(brief.get("key_summary", ""))

    # ── Chord progression
    section_heading("Chord Progression")
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(55, 48, 163)
    pdf.cell(0, 7, brief.get("roman_numeral_progression", ""), ln=True)
    chords = "  ·  ".join(brief.get("main_chords", []))
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(26, 18, 9)
    pdf.cell(0, 6, chords, ln=True)
    pdf.ln(2)
    body_text(brief.get("chord_progression_summary", ""))

    # ── Song structure
    section_heading("Song Structure")
    for item in brief.get("song_structure", []):
        pdf.set_font("Helvetica", 'B', 10)
        pdf.set_text_color(55, 48, 163)
        pdf.cell(40, 6, item.get("section", ""), ln=False)
        pdf.set_font("Helvetica", '', 9)
        pdf.set_text_color(92, 78, 58)
        pdf.cell(35, 6, item.get("timing", ""), ln=False)
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(26, 18, 9)
        pdf.cell(0, 6, item.get("notes", ""), ln=True)
    pdf.ln(4)

    # ── Repeat structure
    section_heading("Repeat & Flow")
    body_text(brief.get("repeat_structure", ""))

    # ── Harmony notes
    section_heading("Harmony Notes")
    body_text(brief.get("harmony_notes", ""))

    # ── Director notes
    section_heading("Director's Notes")
    body_text(brief.get("director_notes", ""))

    # ── Lyrics
    section_heading("Lyrics")
    for section in brief.get("lyrics_by_section", []):
        pdf.set_font("Helvetica", 'B', 10)
        pdf.set_text_color(55, 48, 163)
        pdf.cell(0, 6, section.get("section", "").upper(), ln=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(26, 18, 9)
        pdf.multi_cell(0, 5, section.get("lyrics", ""))
        pdf.ln(4)

    # ── Footer
    pdf.set_y(-18)
    pdf.set_font("Helvetica", 'I', 8)
    pdf.set_text_color(158, 142, 120)
    pdf.cell(0, 5, f"Selah — {brief.get('song_title', '')}  ·  Generated {datetime.now().strftime('%d %B %Y')}", align='C')

    return bytes(pdf.output())


# ── Sidebar ──────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="selah-logo"><span class="selah-logo-lamed">ל</span>SELAH</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-family:\'DM Sans\',sans-serif;font-size:12px;color:#9E8E78;margin-top:-4px;margin-bottom:24px;">Before you lead a choir, take a Selah.</p>',
            unsafe_allow_html=True
        )

        st.divider()

        if st.button("＋  Analyse a New Song", use_container_width=True):
            st.session_state.current_screen = "upload"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🎵  My Songs", use_container_width=True):
            st.session_state.current_screen = "dashboard"
            st.rerun()

        if st.session_state.current_brief:
            if st.button("📄  Current Brief", use_container_width=True):
                st.session_state.current_screen = "brief"
                st.rerun()

        st.divider()

        if st.button("⚙️  Settings", use_container_width=True):
            st.session_state.current_screen = "settings"
            st.rerun()

        # User info
        st.markdown("<br>" * 3, unsafe_allow_html=True)
        st.markdown(
            f'<p style="font-size:12px;color:#9E8E78;">Signed in as<br>'
            f'<strong style="color:#5C4E3A;">{st.session_state.user_email}</strong></p>',
            unsafe_allow_html=True
        )
        if st.button("Sign out", use_container_width=False):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            init_state()
            st.rerun()


# ── Screen: Login ────────────────────────────────────────────────────────────

def screen_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Logo
        st.markdown(
            '<div style="text-align:center;margin-bottom:8px;">'
            '<span style="font-family:\'Barlow Condensed\',sans-serif;font-weight:600;'
            'font-size:48px;letter-spacing:0.12em;color:#3730A3;">ל SELAH</span>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="text-align:center;font-family:\'DM Sans\',sans-serif;'
            'font-size:14px;color:#9E8E78;margin-bottom:40px;">'
            'Before you lead a choir, take a Selah.</p>',
            unsafe_allow_html=True
        )

        with st.container():
            st.markdown('<div class="selah-card">', unsafe_allow_html=True)
            st.markdown("### Sign in to Selah")

            email = st.text_input("Email address", placeholder="you@church.org", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Sign in", use_container_width=True):
                    if email and password:
                        # Prototype: accept any credentials
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_name = email.split("@")[0].replace(".", " ").title()
                        st.session_state.current_screen = "dashboard"
                        st.rerun()
                    else:
                        st.error("Please enter your email and password.")
            with col_b:
                if st.button("Create account", use_container_width=True):
                    if email and password:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_name = email.split("@")[0].replace(".", " ").title()
                        st.session_state.current_screen = "dashboard"
                        st.rerun()
                    else:
                        st.error("Please enter your email and password.")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<p style="text-align:center;font-size:12px;color:#9E8E78;margin-top:24px;">'
            'Prototype — authentication via Supabase in production.</p>',
            unsafe_allow_html=True
        )


# ── Screen: Dashboard ────────────────────────────────────────────────────────

def screen_dashboard():
    st.markdown(f'<h1 style="font-family:\'Cormorant Garamond\',serif;font-size:36px;color:#1A1209;">My Songs</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#9E8E78;margin-top:-12px;margin-bottom:32px;">Welcome back, {st.session_state.user_name}.</p>', unsafe_allow_html=True)

    if not st.session_state.song_library:
        # Empty state
        st.markdown('<br>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="text-align:center;padding:48px 0;">'
                '<div style="font-size:48px;margin-bottom:16px;">ל</div>'
                '<p style="font-family:\'Cormorant Garamond\',serif;font-size:22px;color:#5C4E3A;">Upload your first song.</p>'
                '<p style="font-size:14px;color:#9E8E78;">We\'ll handle the rest.</p>'
                '</div>',
                unsafe_allow_html=True
            )
            if st.button("Analyse a Song", use_container_width=True):
                st.session_state.current_screen = "upload"
                st.rerun()
    else:
        # Song grid
        if st.button("＋  Analyse a New Song"):
            st.session_state.current_screen = "upload"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, song in enumerate(reversed(st.session_state.song_library)):
            with cols[i % 3]:
                st.markdown(
                    f'<div class="selah-card">'
                    f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:20px;font-weight:700;color:#1A1209;margin-bottom:4px;">{song["title"]}</div>'
                    f'<div style="font-size:12px;color:#9E8E78;margin-bottom:16px;">{song["date"]}</div>'
                    f'<span class="badge-key">{song["key"]}</span>'
                    f'<span class="badge-bpm">{song["bpm"]} BPM</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if st.button("View Brief", key=f"view_{i}", use_container_width=True):
                    st.session_state.current_brief = song["brief"]
                    st.session_state.current_screen = "brief"
                    st.rerun()


# ── Screen: Upload ───────────────────────────────────────────────────────────

def screen_upload():
    st.markdown('<h1 style="font-family:\'Cormorant Garamond\',serif;font-size:36px;">Analyse a Song</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9E8E78;margin-top:-12px;margin-bottom:32px;">Upload an audio file and Selah will handle the rest.</p>', unsafe_allow_html=True)

    col_main, col_config = st.columns([3, 2])

    with col_main:
        uploaded_file = st.file_uploader(
            "Drop an audio file here, or click to browse",
            type=["mp3", "wav", "m4a", "aac", "flac"],
            help="Accepted formats: MP3, WAV, M4A, AAC, FLAC · Max 50MB",
        )

        if uploaded_file:
            size_mb = uploaded_file.size / (1024 * 1024)
            if size_mb > 50:
                st.markdown(
                    '<div class="status-error">We couldn\'t accept that file. It exceeds the 50MB limit.</div>',
                    unsafe_allow_html=True
                )
                return

            st.markdown(
                f'<div class="status-success">'
                f'<strong>{uploaded_file.name}</strong> — {size_mb:.1f} MB · ready to analyse.'
                f'</div>',
                unsafe_allow_html=True
            )

            song_title = st.text_input(
                "Song title",
                value=uploaded_file.name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title(),
                placeholder="e.g. Way Maker",
            )

    with col_config:
        st.markdown('<div class="selah-card">', unsafe_allow_html=True)
        st.markdown("#### API Configuration")
        st.caption("These keys are used only for this session and never stored.")

        assemblyai_key = st.text_input(
            "AssemblyAI API Key",
            type="password",
            placeholder="Enter your AssemblyAI key",
            help="Get a free key at assemblyai.com — 100 hours free.",
            key="assemblyai_key"
        )
        claude_key = st.text_input(
            "Google AI API Key",
            type="password",
            placeholder="Enter your Gemini API key",
            help="Get a free key at aistudio.google.com",
            key="claude_key"
        )

        st.markdown("#### Options")
        notation = st.radio(
            "Chord notation",
            ["Both (Roman + Plain names)", "Plain names only", "Roman numerals only"],
            index=0,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if uploaded_file and st.button("Analyse Song →", use_container_width=False):
        if not assemblyai_key:
            st.error("An AssemblyAI API key is required for lyrics transcription.")
            return
        if not claude_key:
            st.error("An Anthropic API key is required to generate the Song Brief.")
            return

        st.session_state.pending_upload = uploaded_file
        st.session_state.pending_title = song_title
        st.session_state.pending_assemblyai_key = assemblyai_key
        st.session_state.pending_claude_key = claude_key
        st.session_state.current_screen = "analysis"
        st.rerun()


# ── Screen: Analysis ─────────────────────────────────────────────────────────

def screen_analysis():
    st.markdown('<h1 style="font-family:\'Cormorant Garamond\',serif;font-size:36px;">Reading the Music</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9E8E78;margin-top:-12px;margin-bottom:32px;">This takes about two minutes.</p>', unsafe_allow_html=True)

    uploaded_file = st.session_state.get("pending_upload")
    song_title = st.session_state.get("pending_title", "Untitled")
    assemblyai_key = st.session_state.get("pending_assemblyai_key", "")
    claude_key = st.session_state.get("pending_claude_key", "")

    if not uploaded_file:
        st.warning("No file found. Please upload a song first.")
        if st.button("← Back to upload"):
            st.session_state.current_screen = "upload"
            st.rerun()
        return

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Animated Lamed mark
        st.markdown(
            '<div style="text-align:center;font-size:80px;color:#3730A3;margin:32px 0 24px;">ל</div>',
            unsafe_allow_html=True
        )

        progress_bar = st.progress(0, text="Preparing audio...")
        status_box = st.empty()

        try:
            import tempfile

            # Save file to disk
            status_box.markdown(
                '<div class="status-processing">Saving audio file for processing…</div>',
                unsafe_allow_html=True
            )
            progress_bar.progress(10, text="Saving audio...")
            time.sleep(0.3)

            suffix = "." + uploaded_file.name.rsplit(".", 1)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # ── Step 1: Librosa
            status_box.markdown(
                '<div class="status-processing">Detecting key, tempo, and chord progressions…</div>',
                unsafe_allow_html=True
            )
            progress_bar.progress(25, text="Music analysis (Librosa)...")

            librosa_data = analyse_with_librosa(tmp_path)
            progress_bar.progress(50, text="Music analysis complete.")
            status_box.markdown(
                f'<div class="status-success">Key detected: <strong>{librosa_data["key"]}</strong> · '
                f'Tempo: <strong>{librosa_data["tempo_bpm"]} BPM</strong></div>',
                unsafe_allow_html=True
            )
            time.sleep(0.5)

            # ── Step 2: AssemblyAI
            status_box.markdown(
                '<div class="status-processing">Transcribing lyrics and identifying song sections…</div>',
                unsafe_allow_html=True
            )
            progress_bar.progress(55, text="Transcription (AssemblyAI)...")

            transcription_data = transcribe_with_assemblyai(tmp_path, assemblyai_key)
            progress_bar.progress(80, text="Transcription complete.")
            status_box.markdown(
                f'<div class="status-success">Transcription complete — '
                f'{len(transcription_data["words"])} words, '
                f'{len(transcription_data["chapters"])} sections detected.</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.5)

            # ── Step 3: Gemini
            status_box.markdown(
                '<div class="status-processing">Structuring your Song Brief…</div>',
                unsafe_allow_html=True
            )
            progress_bar.progress(85, text="Building Song Brief (Gemini 1.5 Pro)...")

            brief = build_song_brief_with_gemini(song_title, librosa_data, transcription_data, claude_key)
            brief["_raw_librosa"] = librosa_data
            brief["_raw_transcription"] = transcription_data

            progress_bar.progress(100, text="Complete.")
            status_box.markdown(
                '<div class="status-success">Your Song Brief is ready.</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.8)

            # Save to library
            st.session_state.song_library.append({
                "title": brief.get("song_title", song_title),
                "key": brief.get("key", librosa_data["key"]),
                "bpm": brief.get("tempo_bpm", librosa_data["tempo_bpm"]),
                "date": datetime.now().strftime("%d %b %Y"),
                "brief": brief,
            })
            st.session_state.current_brief = brief

            # Cleanup
            os.unlink(tmp_path)

            st.session_state.current_screen = "brief"
            st.rerun()

        except Exception as e:
            progress_bar.empty()
            st.session_state.analysis_error = str(e)
            st.markdown(
                f'<div class="status-error">We couldn\'t complete the analysis.<br>'
                f'<strong>Error:</strong> {e}</div>',
                unsafe_allow_html=True
            )
            if st.button("← Try again"):
                st.session_state.current_screen = "upload"
                st.rerun()


# ── Screen: Song Brief ───────────────────────────────────────────────────────

def screen_brief():
    brief = st.session_state.current_brief
    if not brief:
        st.warning("No Song Brief loaded.")
        if st.button("← Back to My Songs"):
            st.session_state.current_screen = "dashboard"
            st.rerun()
        return

    # ── Header
    col_title, col_actions = st.columns([3, 1])
    with col_title:
        st.markdown(
            f'<div class="brief-title">{brief.get("song_title", "Song Brief")}</div>'
            f'<div class="brief-subtitle">Generated {datetime.now().strftime("%d %B %Y")} · Selah Song Brief</div>',
            unsafe_allow_html=True
        )
    with col_actions:
        st.markdown("<br>", unsafe_allow_html=True)
        pdf_bytes = generate_pdf(brief) if FPDF_AVAILABLE else None
        if pdf_bytes:
            st.download_button(
                "⬇ Download PDF",
                data=pdf_bytes,
                file_name=f"selah-{brief.get('song_title','brief').lower().replace(' ','-')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.info("Install fpdf2 to enable PDF export.")

    st.divider()

    # ── Key metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div style="text-align:center;"><div class="badge-key">{brief.get("key","—")}</div><div style="font-size:11px;color:#9E8E78;margin-top:6px;font-family:\'DM Sans\',sans-serif;">KEY</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div style="text-align:center;"><div class="badge-bpm">{brief.get("tempo_bpm","—")}</div><div style="font-size:11px;color:#9E8E78;margin-top:6px;font-family:\'DM Sans\',sans-serif;">BPM</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div style="text-align:center;"><div class="badge-bpm">{brief.get("time_signature","—")}</div><div style="font-size:11px;color:#9E8E78;margin-top:6px;font-family:\'DM Sans\',sans-serif;">TIME SIG</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div style="text-align:center;"><div class="badge-bpm">{brief.get("duration","—")}</div><div style="font-size:11px;color:#9E8E78;margin-top:6px;font-family:\'DM Sans\',sans-serif;">DURATION</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two-column layout
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Overview
        st.markdown('<div class="brief-section-heading">Overview</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-family:\'DM Sans\',sans-serif;font-size:15px;line-height:1.7;color:#1A1209;">{brief.get("key_summary","")}</p>', unsafe_allow_html=True)

        # Chord Progression
        st.markdown('<div class="brief-section-heading">Chord Progression</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:22px;color:#3730A3;font-weight:500;margin-bottom:8px;">'
            f'{brief.get("roman_numeral_progression","")}</div>',
            unsafe_allow_html=True
        )
        chords_html = "".join([f'<span class="badge-chord">{c}</span>' for c in brief.get("main_chords", [])])
        st.markdown(f'<div style="margin-bottom:12px;">{chords_html}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<p style="font-family:\'DM Sans\',sans-serif;font-size:14px;color:#5C4E3A;line-height:1.6;">'
            f'{brief.get("chord_progression_summary","")}</p>',
            unsafe_allow_html=True
        )

        # Chord timeline
        raw_librosa = brief.get("_raw_librosa", {})
        if raw_librosa.get("chord_timeline"):
            with st.expander("Chord Timeline (with timestamps)"):
                header_cols = st.columns([1, 2, 2])
                header_cols[0].markdown("**Time**")
                header_cols[1].markdown("**Chord**")
                header_cols[2].markdown("**Est. Function**")
                for entry in raw_librosa["chord_timeline"]:
                    r = st.columns([1, 2, 2])
                    r[0].markdown(f'<span class="chord-time">{entry["time_label"]}</span>', unsafe_allow_html=True)
                    r[1].markdown(f'<span class="badge-chord">{entry["chord"]}</span>', unsafe_allow_html=True)
                    r[2].markdown(f'<span style="font-size:12px;color:#9E8E78;">—</span>', unsafe_allow_html=True)

        # Harmony
        st.markdown('<div class="brief-section-heading">Harmony Notes</div>', unsafe_allow_html=True)
        st.markdown(
            f'<p style="font-family:\'DM Sans\',sans-serif;font-size:15px;line-height:1.7;color:#1A1209;">{brief.get("harmony_notes","")}</p>',
            unsafe_allow_html=True
        )

        # Director's Notes
        st.markdown('<div class="brief-section-heading">Director\'s Notes</div>', unsafe_allow_html=True)
        st.markdown(
            f'<p style="font-family:\'DM Sans\',sans-serif;font-size:15px;line-height:1.7;color:#1A1209;">{brief.get("director_notes","")}</p>',
            unsafe_allow_html=True
        )

    with col_right:
        # Song Structure
        st.markdown('<div class="brief-section-heading">Song Structure</div>', unsafe_allow_html=True)
        for item in brief.get("song_structure", []):
            st.markdown(
                f'<div class="selah-card" style="padding:14px 18px;margin-bottom:8px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">'
                f'<span class="badge-section">{item.get("section","")}</span>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:#9E8E78;">{item.get("timing","")}</span>'
                f'</div>'
                f'<div style="font-size:13px;color:#5C4E3A;line-height:1.5;">{item.get("notes","")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Repeat structure
        st.markdown('<div class="brief-section-heading">Repeat & Flow</div>', unsafe_allow_html=True)
        st.markdown(
            f'<p style="font-family:\'DM Sans\',sans-serif;font-size:14px;line-height:1.6;color:#5C4E3A;">{brief.get("repeat_structure","")}</p>',
            unsafe_allow_html=True
        )

    # ── Lyrics (full width)
    st.markdown('<div class="brief-section-heading">Lyrics</div>', unsafe_allow_html=True)
    for section in brief.get("lyrics_by_section", []):
        st.markdown(
            f'<div class="lyrics-section">'
            f'<div class="lyrics-label">{section.get("section","").upper()}</div>'
            f'<div class="lyrics-text">{section.get("lyrics","")}</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# ── Screen: Settings ─────────────────────────────────────────────────────────

def screen_settings():
    st.markdown('<h1 style="font-family:\'Cormorant Garamond\',serif;font-size:36px;">Settings</h1>', unsafe_allow_html=True)

    with st.container():
        st.markdown("#### Profile")
        name = st.text_input("Your name", value=st.session_state.user_name)
        church = st.text_input("Church / Organisation", placeholder="e.g. Grace Community Church")
        notation_pref = st.selectbox(
            "Default chord notation",
            ["Both (Roman + Plain names)", "Plain names only", "Roman numerals only"]
        )

        st.divider()
        st.markdown("#### API Keys")
        st.caption("Saved keys are stored in session only and cleared on sign-out.")
        aai_key = st.text_input("AssemblyAI API Key", type="password", placeholder="Paste key here")
        claude_key = st.text_input("Google AI API Key (Gemini)", type="password", placeholder="Paste key here")

        st.divider()
        st.markdown("#### Data")
        st.caption("In production, audio files are deleted after Song Brief generation. Your Song Briefs are retained in your library.")
        if st.button("Clear song library", type="secondary"):
            st.session_state.song_library = []
            st.session_state.current_brief = None
            st.success("Library cleared.")

        if st.button("Save settings"):
            st.session_state.user_name = name
            if aai_key:
                st.session_state.assemblyai_key = aai_key
            if claude_key:
                st.session_state.claude_key = claude_key
            st.success("Settings saved.")


# ── Router ───────────────────────────────────────────────────────────────────

if not st.session_state.authenticated:
    screen_login()
else:
    render_sidebar()
    screen = st.session_state.current_screen

    if screen == "dashboard":
        screen_dashboard()
    elif screen == "upload":
        screen_upload()
    elif screen == "analysis":
        screen_analysis()
    elif screen == "brief":
        screen_brief()
    elif screen == "settings":
        screen_settings()
    else:
        screen_dashboard()
