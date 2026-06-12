# auth.py

This file handles user authentication, including login functionality.

## login

```python
def login(body: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user, token = AuthService(db).login(body.email, body.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return AuthResponse(user_id=user.id, email=user.email, access_token=token)
```

The `login` function authenticates a user with the provided credentials.

**Parameters:**
- `body` (`RegisterRequest`): An object containing the user's email and password.
- `db` (`Session`, optional): Database session dependency. Defaults to `Depends(get_db)`.

**Returns:**
- `AuthResponse`: An object containing the user's ID, email, and access token upon successful login.

**Raises:**
- `HTTPException`: Raises an `HTTPException` with status `401 UNAUTHORIZED` if `InvalidCredentialsError` occurs during login.
