import os
import sys
import time
from huggingface_hub import snapshot_download
from huggingface_hub.utils import HfHubHTTPError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
# Use HF_HOME from environment if set, otherwise default to a local cache.
# This makes the script more flexible and respects user configuration.
DEFAULT_CACHE_DIR = "./hf_cache"
HF_CACHE_HOME = os.path.abspath(os.getenv("HF_HOME", DEFAULT_CACHE_DIR))

# Ensure the cache directory exists
os.makedirs(HF_CACHE_HOME, exist_ok=True)
logger.info(f"Using Hugging Face cache directory: {HF_CACHE_HOME}")

# --- Models to Download ---
MODELS = {
    "transcription": "Systran/faster-whisper-small",
    "embedding": "sentence-transformers/all-MiniLM-L6-v2"
}
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 10

# --- Download Logic ---
def download_models():
    """
    Downloads the required models from Hugging Face Hub, with retries for robustness.
    """
    for model_type, repo_id in MODELS.items():
        logger.info(f"--- Ensuring {model_type} model ({repo_id}) is downloaded ---")

        # First, try to find the model in the local cache. This is much faster.
        try:
            snapshot_download(
                repo_id=repo_id,
                cache_dir=HF_CACHE_HOME,
                local_files_only=True
            )
            logger.info(f"Model '{repo_id}' found in local cache. No download needed.")
            continue # Move to the next model
        except FileNotFoundError:
            logger.info(f"Model '{repo_id}' not found locally. Starting download...")
        except Exception as e:
            logger.error(f"An unexpected error occurred while checking local cache for {repo_id}: {e}")
            # If we can't even check the cache, we should probably stop.
            raise RuntimeError(f"Failed to check local cache for {repo_id}") from e

        # If not found locally, proceed with download attempts.
        for attempt in range(MAX_RETRIES):
            try:
                snapshot_download(
                    repo_id=repo_id,
                    cache_dir=HF_CACHE_HOME,
                    local_files_only=False # Actually download
                )
                logger.info(f"Successfully downloaded {repo_id}")
                break # Success, move to the next model
            except HfHubHTTPError as e:
                logger.warning(f"HTTP Error during download (Attempt {attempt + 1}/{MAX_RETRIES}): {e}. Retrying in {RETRY_DELAY_SECONDS}s...")
                time.sleep(RETRY_DELAY_SECONDS)
            except Exception as e:
                logger.error(f"An unexpected error occurred during download (Attempt {attempt + 1}/{MAX_RETRIES}): {e}. Retrying in {RETRY_DELAY_SECONDS}s...")
                time.sleep(RETRY_DELAY_SECONDS)

        else: # This 'else' belongs to the 'for' loop, executed if the loop completes without 'break'
            logger.critical(f"Failed to download model {repo_id} after {MAX_RETRIES} attempts. Please check your network connection.")
            raise RuntimeError(f"Failed to download model {repo_id}")


if __name__ == "__main__":
    logger.info("Starting model download/verification process...")
    try:
        download_models()
        logger.info("All models are available locally.")
    except Exception as e:
        logger.critical(f"The model download process failed. Error: {e}")
        # Exit with a non-zero code to indicate failure, useful for scripting
        sys.exit(1)
