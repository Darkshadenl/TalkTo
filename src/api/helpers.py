from fastapi import Header, HTTPException
from pathlib import Path
from ..core.services import AuthService
from ..core.config import settings
from ..utils.helpers import normalize_path

# Initialize services
auth_service = AuthService()


async def verify_token(x_api_token: str = Header(..., alias="X-API-Token")) -> None:
    """
    Dependency to verify API token for protected endpoints.
    Raises HTTPException if token is invalid.
    """
    if not await auth_service.validate_token(x_api_token):
        raise HTTPException(
            status_code=401,
            detail="Invalid API token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def resolve_folder_path(folder_id: str, relative_path: str) -> Path:
    """
    Resolve the full path for a given folder ID and relative path.

    Args:
        folder_id (str): The ID of the watched folder
        relative_path (str): The relative path within the folder

    Raises:
        HTTPException: If folder ID is invalid or path is outside the folder

    Returns:
        Path: The resolved full path
    """
    if folder_id not in settings.WATCHED_FOLDERS_MAP:
        raise HTTPException(status_code=404, detail=f"Folder ID {folder_id} not found")

    base_path = settings.WATCHED_FOLDERS_MAP[folder_id]
    full_path = base_path / normalize_path(relative_path)

    # Ensure the resolved path is within the base path
    if not full_path.is_relative_to(base_path):
        raise HTTPException(
            status_code=400,
            detail="Invalid path: Cannot access files outside the watched folder",
        )

    return full_path
