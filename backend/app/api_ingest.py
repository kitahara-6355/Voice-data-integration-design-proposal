# backend/app/api_ingest.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

# Absolute imports from the project root
from backend.app.services.transcribe import transcribe_file
from backend.app.services.embed_index import embed_and_index

router = APIRouter()

# Define the path to the storage directory relative to this file's location
STORAGE_BASE_PATH = Path(__file__).resolve().parent.parent.parent / "storage" / "processed" / "audio"

@router.post('/audio')
async def upload_audio(file: UploadFile = File(...)):
    """
    Accepts an audio file, saves it, transcribes it, and indexes the text.
    """
    try:
        # Ensure the target directory exists
        STORAGE_BASE_PATH.mkdir(parents=True, exist_ok=True)

        # Create a safe path for the uploaded file
        save_path = STORAGE_BASE_PATH / file.filename

        # Save the uploaded file
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process the file
        # Note: transcribe_file and embed_and_index are placeholders for now
        text, segments = transcribe_file(str(save_path))
        embed_and_index(segments, source=file.filename)

        return {'status': 'ok', 'filename': file.filename, 'segments_found': len(segments)}

    except Exception as e:
        # Log the error for debugging
        print(f"Error processing file {file.filename}: {e}")
        # Raise a proper HTTP exception
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {e}")
    finally:
        # Close the file to release resources
        if file:
            await file.close()
