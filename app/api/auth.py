"""OAuth2 + PKCE authorization endpoints."""

from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import RedirectResponse

from app.services.oauth_service import oauth_service
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

In-memory store for PKCE verifiers (use Redis in production)
_temp_store: dict = {}

@router.get("/login")
async def login():
"""Initiate OAuth2 + PKCE flow."""
auth_data = oauth_service.get_authorization_url()

# Store verifier temporarily (use Redis with TTL in production)
_temp_store[auth_data["state"]] = {
"verifier": auth_data["code_verifier"],
"created_at": import('datetime').datetime.now(import('datetime').timezone.utc).isoformat(),
}

return RedirectResponse(url=auth_data["authorization_url"])

@router.get("/logout")
async def logout(response: Response):
"""Clear auth cookies."""
response.delete_cookie("access_token")
response.delete_cookie("refresh_token")
return {"message": "Logged out successfully"}

