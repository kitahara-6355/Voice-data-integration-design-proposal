from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter()

# Define the base path to the audio storage directory
# This should be an absolute path for security and reliability.
# We will calculate it once and reuse it.
STORAGE_BASE_PATH = Path(__file__).resolve().parent.parent.parent / "storage" / "processed" / "audio"

def get_audio_file_path(filename: str) -> Path:
    """
    Validates and resolves the path to an audio file.
    This function helps prevent directory traversal attacks.
    """
    # Sanitize filename to prevent directory traversal
    # os.path.basename will return only the final component of the path
    safe_basename = os.path.basename(filename)

    file_path = (STORAGE_BASE_PATH / safe_basename).resolve()

    # Security check: Ensure the resolved path is still within our storage directory
    if not file_path.is_file() or not str(file_path).startswith(str(STORAGE_BASE_PATH.resolve())):
        raise HTTPException(status_code=404, detail="File not found")

    return file_path

@router.get("/{filename}")
async def get_audio_file(file_path: Path = Depends(get_audio_file_path)):
    """
    Serves a specific audio file from the processed storage directory.
    Includes security checks to prevent accessing files outside the intended directory.
    """
    return FileResponse(
        path=file_path,
        media_type='audio/mpeg', # Common for .m4a files
        filename=file_path.name
    )
