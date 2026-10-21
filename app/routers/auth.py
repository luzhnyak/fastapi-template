from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.api.dependencies import get_auth_service, get_current_user
from app.core.config import settings
from app.domain.entities.user import User
from app.schemas.auth import (
    Auth0Token,
    AuthResponse,
    GoogleAuthRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        "refresh_token",
        token,
        httponly=True,
        secure=settings.app.COOKIE_SECURE,
        samesite="strict",
        path="/auth",
        max_age=60 * 60 * 24 * settings.app.REFRESH_TOKEN_EXPIRE_DAYS,
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest, response: Response, service: AuthService = Depends(get_auth_service)
):
    result = await service.register(data)
    set_refresh_cookie(response, result.refresh_token)
    return result


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest, response: Response, service: AuthService = Depends(get_auth_service)
):
    result = await service.login(data)
    set_refresh_cookie(response, result.refresh_token)
    return result


@router.get("/me", response_model=AuthResponse)
async def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    return {
        "access_token": request.headers["Authorization"].split()[1],
        "token_type": "Bearer",
        "user": current_user,
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: Request, response: Response, service: AuthService = Depends(get_auth_service)
):
    result = await service.refresh_token(request.cookies.get("refresh_token"))
    set_refresh_cookie(response, result.refresh_token)
    return result


@router.post("/google", response_model=AuthResponse)
async def google_login(
    data: GoogleAuthRequest, response: Response, service: AuthService = Depends(get_auth_service)
):
    result = await service.google_login(data.code)
    set_refresh_cookie(response, result.refresh_token)
    return result


@router.post("/auth0-login", response_model=TokenResponse, deprecated=True)
async def auth0_login(data: Auth0Token):
    # Preserve an explicit response for the old placeholder endpoint.
    raise HTTPException(status_code=503, detail="Auth0 login is not implemented")


@router.post("/logout")
async def logout(response: Response):
    for path in ("/auth", "/"):
        response.delete_cookie(
            "refresh_token",
            path=path,
            httponly=True,
            secure=settings.app.COOKIE_SECURE,
            samesite="strict",
        )
    return {"detail": "Logged out successfully"}
