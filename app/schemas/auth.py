from pydantic import BaseModel

from app.schemas.user import SignInRequest, SignUpRequest, UserResponse


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class Token(TokenResponse):
    refresh_token: str


class Auth0Token(BaseModel):
    token: str


class RegisterRequest(SignUpRequest):
    pass


class LoginRequest(SignInRequest):
    pass


class AuthResponse(TokenResponse):
    user: UserResponse


class GoogleAuthRequest(BaseModel):
    code: str
