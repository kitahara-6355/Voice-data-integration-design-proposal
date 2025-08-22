import os
from huggingface_hub import snapshot_download
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
# Define a local cache directory within the project
cache_dir = "./hf_cache"
# Set the Hugging Face home directory to our local cache
os.environ['HF_HOME'] = os.path.abspath(cache_dir)

# Ensure the cache directory exists
os.makedirs(cache_dir, exist_ok=True)
logger.info(f"Using Hugging Face cache directory: {os.path.abspath(cache_dir)}")

# --- Models to Download ---
models = {
    "transcription": "Systran/faster-whisper-small",
    "embedding": "sentence-transformers/all-MiniLM-L6-v2"
}

# --- Download Logic ---
def download_models():
    """
    Downloads the required models from Hugging Face Hub into the local cache.
    """
    for model_type, repo_id in models.items():
        logger.info(f"--- Downloading {model_type} model: {repo_id} ---")
        try:
            snapshot_download(
                repo_id=repo_id,
                cache_dir=cache_dir,
                # Using a local files only flag after first download can speed things up,
                # but for the initial download we need to connect to the hub.
                # local_files_only=False,
            )
            logger.info(f"Successfully downloaded {repo_id}")
        except Exception as e:
            logger.error(f"Failed to download model {repo_id}. Error: {e}")
            # Decide if you want to stop or continue
            # For now, we'll stop on the first failure.
            raise

if __name__ == "__main__":
    logger.info("Starting model download process...")
    download_models()
    logger.info("All models have been downloaded successfully.")
