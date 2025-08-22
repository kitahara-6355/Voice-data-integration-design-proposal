# backend/app/api_search.py
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Any, Dict

# Absolute imports from the project root
from backend.app.services.embed_index import query

router = APIRouter()

class QueryRequest(BaseModel):
    """Request model for a search query."""
    q: str = Field(..., description="The search query string.")
    top: int = Field(default=5, gt=0, le=20, description="The number of results to return.")

class Hit(BaseModel):
    """Represents a single search result hit."""
    id: str
    score: float
    payload: Dict[str, Any]
    document: str


class QueryResponse(BaseModel):
    """Response model for a search query."""
    hits: List[Dict] # Using Dict for now, ChromaDB returns a list of dicts

@router.post('/', response_model=QueryResponse)
async def search(request: QueryRequest):
    """
    Accepts a search query and returns the top matching results from the vector store.
    """
    # Note: the 'query' function is a placeholder for now
    hits = query(request.q, top=request.top)
    return {'hits': hits}
