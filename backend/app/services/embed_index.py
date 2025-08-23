# backend/app/services/embed_index.py
import uuid
import logging
from typing import List, Dict, Any
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Attempt to import ChromaDB and set a flag ---
try:
    import chromadb
    CHROMA_OK = True
except ImportError:
    CHROMA_OK = False
    print("ChromaDB not found, will use in-memory search as a fallback.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Global variables for models and data stores ---
model: SentenceTransformer = None
# ChromaDB specific
collection: "chromadb.Collection" = None
# In-memory fallback specific
IN_MEMORY_STORE = []

def load_model_and_db():
    """Initializes the embedding model and the data store (ChromaDB or in-memory)."""
    global model, collection, IN_MEMORY_STORE, CHROMA_OK

    # Load the sentence transformer model (common for both modes)
    if model is None:
        try:
            logger.info("Loading SentenceTransformer model: all-MiniLM-L6-v2...")
            model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.error(f"Fatal: Failed to load SentenceTransformer model: {e}")
            raise e

    # Initialize ChromaDB if available
    if CHROMA_OK:
        if collection is None:
            try:
                logger.info("Initializing ChromaDB client...")
                db_path = str(Path(__file__).resolve().parent.parent.parent / "chroma_db")
                client = chromadb.PersistentClient(path=db_path)
                COLLECTION_NAME = "speechhub"
                collection = client.get_or_create_collection(name=COLLECTION_NAME)
                logger.info(f"ChromaDB client initialized. Collection '{COLLECTION_NAME}' is ready.")
            except Exception as e:
                logger.error(f"Failed to initialize ChromaDB: {e}. Falling back to in-memory store.")
                CHROMA_OK = False # Force fallback

    if not CHROMA_OK:
        logger.warning("Using temporary in-memory search. Search index will be lost on restart.")
        IN_MEMORY_STORE = []


def embed_and_index(segments: List[Dict[str, Any]], source: str = 'unknown'):
    """Embeds text segments and adds them to the active data store."""
    if model is None:
        raise RuntimeError("Embedding model is not initialized.")

    if not segments:
        return

    docs = [seg.get('text') for seg in segments if seg.get('text')]
    if not docs:
        return

    logger.info(f"Embedding {len(docs)} segments for source: {source}")
    embeddings = model.encode(docs, show_progress_bar=False)

    if CHROMA_OK:
        if collection is None:
            raise RuntimeError("ChromaDB is not initialized.")
        ids = [str(uuid.uuid4()) for _ in docs]
        metadatas = [{'source': source, 'start': s.get('start', 0.0), 'end': s.get('end', 0.0)} for s in segments if s.get('text')]
        collection.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embeddings.tolist())
        logger.info("Segments indexed in ChromaDB.")
    else:
        # In-memory fallback
        for i, doc in enumerate(docs):
            IN_MEMORY_STORE.append({
                'id': str(uuid.uuid4()),
                'text': doc,
                'metadata': {'source': source, 'start': segments[i].get('start', 0.0), 'end': segments[i].get('end', 0.0)},
                'vector': embeddings[i]
            })
        logger.info(f"Segments stored in-memory. Total items: {len(IN_MEMORY_STORE)}")


def query(q: str, top: int = 5) -> List[Dict[str, Any]]:
    """Performs a semantic search query against the active data store."""
    if model is None:
        raise RuntimeError("Embedding model is not initialized.")

    logger.info(f"Performing query: '{q}'")
    query_embedding = model.encode(q)

    if CHROMA_OK:
        if collection is None:
            raise RuntimeError("ChromaDB is not initialized.")

        results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=top, include=['metadatas', 'documents', 'distances'])

        hits = []
        if results and results.get('ids') and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                hits.append({
                    "id": results['ids'][0][i],
                    "score": 1 - results['distances'][0][i], # Convert distance to similarity
                    "document": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                })
        logger.info(f"Query returned {len(hits)} hits from ChromaDB.")
        return hits
    else:
        # In-memory fallback search
        if not IN_MEMORY_STORE:
            return []

        vectors = np.array([item['vector'] for item in IN_MEMORY_STORE])
        # Cosine similarity calculation
        scores = np.dot(vectors, query_embedding) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_embedding))

        # Get top k results
        top_k_indices = np.argsort(scores)[-top:][::-1]

        hits = []
        for i in top_k_indices:
            item = IN_MEMORY_STORE[i]
            hits.append({
                "id": item['id'],
                "score": float(scores[i]),
                "document": item['text'],
                "metadata": item['metadata']
            })
        logger.info(f"Query returned {len(hits)} hits from in-memory store.")
        return hits
