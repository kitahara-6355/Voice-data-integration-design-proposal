import os
import time
import logging
import sys

# Ensure the backend app path is in the system path to allow module imports
backend_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))
if backend_app_path not in sys.path:
    sys.path.insert(0, backend_app_path)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_loading():
    """
    Tests the loading time of the ML models to diagnose startup delays.
    """
    # --- Set Environment Variable ---
    # This is crucial to ensure the cached models are used.
    cache_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hf_cache'))
    os.environ['HF_HOME'] = cache_dir
    logger.info(f"Using HF_HOME: {os.environ['HF_HOME']}")

    if not os.path.exists(cache_dir):
        logger.error("Cache directory not found! Please run download_models.py first.")
        return

    # --- Import Services ---
    # We import them here to ensure the environment variable is set first.
    try:
        from services import transcribe, embed_index
    except ImportError as e:
        logger.error(f"Failed to import services. Make sure the script is run from the project root or the path is set correctly. Error: {e}")
        return

    # --- Test Transcription Model ---
    logger.info("--- Testing Transcription Model Loading ---")
    start_time = time.time()
    try:
        transcribe.load_model()
        end_time = time.time()
        logger.info(f"SUCCESS: Transcription model loaded in {end_time - start_time:.2f} seconds.")
    except Exception as e:
        end_time = time.time()
        logger.error(f"FAILED: Transcription model failed to load after {end_time - start_time:.2f} seconds. Error: {e}")
        return # Stop if the first model fails

    # --- Test Embedding Model & DB ---
    logger.info("--- Testing Embedding Model & DB Loading ---")
    start_time = time.time()
    try:
        embed_index.load_model_and_db()
        end_time = time.time()
        logger.info(f"SUCCESS: Embedding model and DB loaded in {end_time - start_time:.2f} seconds.")
    except Exception as e:
        end_time = time.time()
        logger.error(f"FAILED: Embedding model or DB failed to load after {end_time - start_time:.2f} seconds. Error: {e}")

if __name__ == "__main__":
    test_loading()
