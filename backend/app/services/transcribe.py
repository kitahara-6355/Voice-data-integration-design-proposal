# backend/app/services/transcribe.py
from faster_whisper import WhisperModel
import logging
from typing import Tuple, List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Model Loading ---
MODEL_SIZE = "small"
model: WhisperModel = None

def load_model():
    """Loads the transcription model into memory."""
    global model
    if model is None:
        try:
            logger.info(f"Loading faster-whisper model: {MODEL_SIZE}...")
            # For CPU execution, 'int8' is a good balance of speed and quality.
            model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
            logger.info("Whisper model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load whisper model: {e}. Transcription will not be available.")
            # Re-raise the exception to be handled by the startup process
            raise e

def transcribe_file(path: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Transcribes the audio file at the given path using the pre-loaded whisper model.

    Args:
        path (str): The file path to the audio file.

    Returns:
        A tuple containing:
        - The full transcribed text.
        - A list of segment dictionaries, each with 'text', 'start', and 'end' times.
    """
    if model is None:
        raise RuntimeError("Whisper model is not loaded. Call load_model() during application startup.")

    logger.info(f"Starting transcription for: {path}")

    # The transcribe function returns an iterator. We need to convert it to a list.
    segments_iterator, info = model.transcribe(path, language="ja", beam_size=5)

    segments = []
    full_text_parts = []

    for segment in segments_iterator:
        segments.append({
            # faster-whisper does not provide a stable segment ID, so we don't include it.
            "text": segment.text.strip(),
            "start": round(segment.start, 2),
            "end": round(segment.end, 2)
        })
        full_text_parts.append(segment.text)

    full_text = "".join(full_text_parts).strip()

    logger.info(f"Transcription complete for: {path}")
    logger.info(f"Detected language: {info.language} with probability {info.language_probability:.2f}")

    return full_text, segments
