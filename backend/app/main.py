# backend/app/main.py
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from contextlib import asynccontextmanager
import logging

# Absolute imports from the project root
from backend.app import api_ingest
from backend.app import api_search
from backend.app.services import transcribe, embed_index

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load ML models during startup
    logger.info("Application startup: Loading models...")
    try:
        transcribe.load_model()
        embed_index.load_model_and_db()
        logger.info("Models loaded successfully.")
    except Exception as e:
        logger.critical(f"Failed to load models during startup: {e}")
        # Depending on the desired behavior, you might want to exit the app
        # or allow it to run in a degraded state. For now, we log critical error.
    yield
    # Cleanup on shutdown (not used here, but good practice)
    logger.info("Application shutdown.")

app = FastAPI(title="SpeechHub Local API", lifespan=lifespan)

# Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(api_ingest.router, prefix="/api/ingest", tags=["ingest"])
app.include_router(api_search.router, prefix="/api/search", tags=["search"])


# Health check endpoint
@app.get("/api/health")
async def health():
    return {"status": "ok"}

# Serve frontend
# The frontend files are expected to be in ../../frontend relative to this main.py file
# which is located in backend/app
frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"

@app.get("/")
async def read_index():
    index_path = frontend_dir / "index.html"
    if not index_path.exists():
        return Response(content="<h1>Frontend not found</h1><p>Ensure an index.html file exists in the /frontend directory.</p>", status_code=404, media_type="text/html")

    with open(index_path, "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")
