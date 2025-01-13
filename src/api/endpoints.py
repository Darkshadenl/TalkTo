from fastapi import APIRouter, HTTPException
from ..core.services import FileSystemService
from ..core.config import settings
from ..utils.helpers import validate_path
from pathlib import Path

router = APIRouter()
file_service = FileSystemService()

@router.get("/folders/{path:path}")
async def list_folder_contents(path: str):
    # Ensure the path is within BASE_PATH
    full_path = settings.BASE_PATH / path
    if not validate_path(str(full_path)):
        raise HTTPException(
            status_code=400, 
            detail="Invalid path or path outside of allowed directory"
        )
    try:
        return await file_service.list_directory(str(full_path))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/config/watched-folders")
async def get_watched_folders():
    """Return the list of configured watched folders"""
    return settings.WATCHED_FOLDERS