from fastapi import APIRouter, HTTPException, Body, Depends
from ..core.services import FileSystemService, AuthService
from ..core.config import settings
from .helpers import verify_token, resolve_folder_path

router = APIRouter()
file_service = FileSystemService()
auth_service = AuthService()


@router.get("/folders/{folder_id}/{path:path}", dependencies=[Depends(verify_token)])
@router.get("/folders/{folder_id}", dependencies=[Depends(verify_token)])
async def list_folder_contents(folder_id: str, path: str = ""):
    """List contents of a directory within a specific watched folder"""
    try:
        full_path = resolve_folder_path(folder_id, path)
        return await file_service.list_directory(str(full_path))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{folder_id}/{path:path}", dependencies=[Depends(verify_token)])
async def get_file_content(folder_id: str, path: str):
    """Get content of a specific file within a watched folder"""
    try:
        full_path = resolve_folder_path(folder_id, path)
        return await file_service.get_file_content(full_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/files/{folder_id}/{path:path}", dependencies=[Depends(verify_token)])
async def create_file(
    folder_id: str,
    path: str,
    content: str = Body(..., description="File content"),
):
    """Create a new file with content in a specific watched folder"""
    try:
        full_path = resolve_folder_path(folder_id, path)
        success = await file_service.create_file(full_path, content)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create file")
        return {"status": "success", "message": "File created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/files/{folder_id}/{path:path}", dependencies=[Depends(verify_token)])
async def update_file(
    folder_id: str,
    path: str,
    content: str = Body(..., description="New file content"),
):
    """Update an existing file with new content in a specific watched folder"""
    try:
        full_path = resolve_folder_path(folder_id, path)
        success = await file_service.update_file(full_path, content)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update file")
        return {"status": "success", "message": "File updated successfully"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/files/{folder_id}/{path:path}", dependencies=[Depends(verify_token)])
async def delete_file(folder_id: str, path: str):
    """Delete a specific file in a watched folder"""
    try:
        full_path = resolve_folder_path(folder_id, path)
        success = await file_service.delete_file(full_path)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete file")
        return {"status": "success", "message": "File deleted successfully"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config/watched-folders", dependencies=[Depends(verify_token)])
async def get_watched_folders():
    """Return the list of configured watched folders with their IDs"""
    return [
        {
            "id": folder.id,
            "name": folder.name,
            "path": str(folder.path),
            "description": folder.description,
        }
        for folder in settings.WATCHED_FOLDERS
    ]
