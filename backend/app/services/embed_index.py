# backend/app/services/embed_index.py
from sentence_transformers import SentenceTransformer
import chromadb
import uuid
import logging
from typing import List, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Model and DB Client Loading ---
model: SentenceTransformer = None
collection: chromadb.Collection = None

def load_model_and_db():
    """Initializes the embedding model and the ChromaDB client."""
    global model, collection
    if model is None:
        try:
            logger.info("Loading SentenceTransformer model: all-MiniLM-L6-v2...")
            model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model: {e}")
            raise e

    if collection is None:
        try:
            logger.info("Initializing ChromaDB client...")
            db_path = str(Path(__file__).resolve().parent.parent.parent / "chroma_db")
            client = chromadb.PersistentClient(path=db_path)

            COLLECTION_NAME = "speechhub"
            collection = client.get_or_create_collection(name=COLLECTION_NAME)
            logger.info(f"ChromaDB client initialized. Collection '{COLLECTION_NAME}' is ready.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise e

def embed_and_index(segments: List[Dict[str, Any]], source: str = 'unknown'):
    """
    Embeds text segments and adds them to the ChromaDB collection.
    """
    if model is None or collection is None:
        raise RuntimeError("Embedding model or DB is not initialized. Call load_model_and_db() on startup.")

    if not segments:
        logger.warning("embed_and_index called with no segments to process.")
        return

    ids, documents, metadatas = [], [], []

    for seg in segments:
        text = seg.get('text')
        if not text: continue

        ids.append(str(uuid.uuid4()))
        documents.append(text)
        metadatas.append({'source': source, 'start': seg.get('start', 0.0), 'end': seg.get('end', 0.0)})

    if not documents:
        logger.warning("No valid text found in segments to be indexed.")
        return

    logger.info(f"Embedding and indexing {len(documents)} segments for source: {source}")
    embeddings = model.encode(documents, show_progress_bar=False).tolist()

    collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
    logger.info("Segments indexed successfully.")


def query(q: str, top: int = 5) -> List[Dict[str, Any]]:
    """
    Performs a semantic search query against the ChromaDB collection.
    """
    if not model or not collection:
        raise RuntimeError("Embedding model or DB is not initialized. Cannot query.")

    logger.info(f"Performing query: '{q}'")
    query_embedding = model.encode(q).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top,
        include=['metadatas', 'documents', 'distances']
    )

    hits = []
    if results and results.get('ids') and results['ids'][0]:
        for i in range(len(results['ids'][0])):
            hits.append({
                "id": results['ids'][0][i],
                "distance": round(results['distances'][0][i], 4),
                "document": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
            })

    logger.info(f"Query returned {len(hits)} hits.")
    return hits
