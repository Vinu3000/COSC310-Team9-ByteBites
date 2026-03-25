from pydantic import BaseModel

class RegisterRequest(BaseModel):
    """Request body for user registration."""
    username: str
    password: str

class LoginRequest(BaseModel):
    """Request body for user login."""
    username: str
    password: str

class AuthResponse(BaseModel):
    """Response returned after successful login."""
    access_token: str
    token_type: str
