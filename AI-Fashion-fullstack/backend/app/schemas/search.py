"""Search schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class SearchRequest(BaseModel):
    """Search request schema"""
    text: Optional[str] = Field(None, description="Text query")
    k: int = Field(10, ge=1, le=100, description="Number of results")
    text_weight: float = Field(0.7, ge=0.0, le=1.0, description="Text weight for hybrid search")
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")


class Product(BaseModel):
    """Product schema"""
    rank: int
    id: int
    name: str
    category: str
    color: str
    gender: str
    price: float
    description: str
    score: float
    similarity: float


class SearchResponse(BaseModel):
    """Search response schema"""
    total: int
    results: List[Product]
    query_info: Dict[str, Any]
