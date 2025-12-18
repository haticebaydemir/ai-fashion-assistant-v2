"""
SSOT (Single Source of Truth) Schema Definitions
=================================================

This module defines all data structures used across the project.
All notebooks and modules MUST use these schemas for consistency.

Author: AI Fashion Assistant Team
Date: 2025-01-XX
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum
import json


# ============================================================
# ENUMS - Standardized categorical values
# ============================================================

class Intent(str, Enum):
    """User intent types"""
    SEARCH = "search"
    FILTER = "filter"
    COMPARE = "compare"
    RECOMMEND = "recommend"
    COMBINE = "combine"  # Outfit combination
    UNKNOWN = "unknown"


class Gender(str, Enum):
    """Product gender categories"""
    MEN = "Men"
    WOMEN = "Women"
    BOYS = "Boys"
    GIRLS = "Girls"
    UNISEX = "Unisex"


class MasterCategory(str, Enum):
    """Top-level product categories"""
    APPAREL = "Apparel"
    FOOTWEAR = "Footwear"
    ACCESSORIES = "Accessories"
    PERSONAL_CARE = "Personal Care"
    FREE_ITEMS = "Free Items"


class Season(str, Enum):
    """Seasonal categories"""
    SUMMER = "Summer"
    WINTER = "Winter"
    FALL = "Fall"
    SPRING = "Spring"


class Usage(str, Enum):
    """Usage contexts"""
    CASUAL = "Casual"
    FORMAL = "Formal"
    SPORTS = "Sports"
    SMART_CASUAL = "Smart Casual"
    ETHNIC = "Ethnic"
    PARTY = "Party"


# ============================================================
# PRODUCT SCHEMA
# ============================================================

@dataclass
class Product:
    """
    Represents a single product in the catalog.
    
    This is the canonical product representation used throughout the system.
    """
    # Primary key
    id: int
    
    # Product information
    productDisplayName: str
    masterCategory: str
    subCategory: str
    articleType: str
    baseColour: str
    gender: str
    season: str
    year: Optional[int] = None
    usage: Optional[str] = None
    
    # Derived fields
    desc: Optional[str] = None  # Combined text description
    image_path: Optional[str] = None
    
    # Embeddings (added after generation)
    text_embedding: Optional[List[float]] = None
    image_embedding: Optional[List[float]] = None
    hybrid_embedding: Optional[List[float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create from dictionary"""
        return cls(**data)


# ============================================================
# QUERY SCHEMA
# ============================================================

@dataclass
class QueryRecord:
    """
    Represents a user query with normalization and extracted attributes.
    
    This is the canonical query representation.
    """
    # Primary key
    query_id: str
    
    # Query text
    query_text_original: str  # Original user input
    query_text_tr: str        # Turkish normalized
    query_norm: str           # Fully normalized (lowercase, no punct)
    
    # Extracted attributes
    intent: Optional[Intent] = None
    slots: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Rewrites (if applicable)
    rewrites: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        d = asdict(self)
        if self.timestamp:
            d['timestamp'] = self.timestamp.isoformat()
        if self.intent:
            d['intent'] = self.intent.value
        return d
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueryRecord':
        """Create from dictionary"""
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        if 'intent' in data and isinstance(data['intent'], str):
            data['intent'] = Intent(data['intent'])
        return cls(**data)


# ============================================================
# CANDIDATE SCHEMA
# ============================================================

@dataclass
class Candidate:
    """
    Represents a candidate product for a query with retrieval scores.
    
    Used in retrieval and ranking pipelines.
    """
    query_id: str
    product_id: int
    
    # Retrieval scores
    text_score: Optional[float] = None
    image_score: Optional[float] = None
    hybrid_score: Optional[float] = None
    
    # Ranks
    text_rank: Optional[int] = None
    image_rank: Optional[int] = None
    hybrid_rank: Optional[int] = None
    
    # Advanced scores (added in later phases)
    fusion_score: Optional[float] = None      # Phase G
    attr_match_score: Optional[float] = None  # Phase H
    personalization_score: Optional[float] = None
    final_score: Optional[float] = None
    
    # Attribute matches
    attr_matches: Dict[str, bool] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Candidate':
        """Create from dictionary"""
        return cls(**data)


# ============================================================
# GROUND TRUTH SCHEMA
# ============================================================

@dataclass
class GroundTruth:
    """
    Ground truth relevance labels for evaluation.
    
    CRITICAL: Use product_id, NOT product_name!
    """
    query_id: str
    product_id: int  # ❌ NOT product_name!
    
    # Relevance level
    # 0: not relevant
    # 1: relevant
    # 2: highly relevant
    relevance: int = 1
    
    # Metadata
    annotation_source: Optional[str] = None  # 'manual', 'weak', 'synthetic'
    annotator: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GroundTruth':
        """Create from dictionary"""
        return cls(**data)


# ============================================================
# USER PROFILE SCHEMA
# ============================================================

@dataclass
class UserProfile:
    """User profile for personalization"""
    user_id: str
    
    # Preferences
    style_preference: Optional[str] = None  # casual, formal, sports
    color_preferences: List[str] = field(default_factory=list)
    size_range: List[str] = field(default_factory=list)
    budget_range: Optional[str] = None  # low, mid, high
    
    # Embeddings
    user_embedding: Optional[List[float]] = None
    
    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        d = asdict(self)
        if self.created_at:
            d['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            d['updated_at'] = self.updated_at.isoformat()
        return d


@dataclass
class UserEvent:
    """User interaction event"""
    event_id: str
    user_id: str
    product_id: int
    event_type: str  # view, click, favorite, add_to_cart
    timestamp: datetime
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d


# ============================================================
# NORMALIZATION FUNCTIONS
# ============================================================

def normalize_text(text: str, mode: str = 'standard') -> str:
    """
    Single Source of Truth for text normalization.
    
    Args:
        text: Input text
        mode: Normalization mode
            - 'standard': lowercase + strip
            - 'aggressive': + remove punctuation
            - 'turkish_aware': + Turkish char normalization
    
    Returns:
        Normalized text
    """
    import re
    
    text = text.lower().strip()
    
    if mode in ['aggressive', 'turkish_aware']:
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
    
    if mode == 'turkish_aware':
        # Turkish character normalization (optional)
        tr_map = {
            'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
            'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
        }
        for tr_char, en_char in tr_map.items():
            text = text.replace(tr_char, en_char)
    
    return text.strip()


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_product(product: Product) -> bool:
    """Validate product schema"""
    assert product.id is not None, "Product ID is required"
    assert product.productDisplayName, "Product name is required"
    assert product.masterCategory, "Master category is required"
    return True


def validate_query(query: QueryRecord) -> bool:
    """Validate query schema"""
    assert query.query_id, "Query ID is required"
    assert query.query_text_original, "Query text is required"
    return True


def validate_candidate(candidate: Candidate) -> bool:
    """Validate candidate schema"""
    assert candidate.query_id, "Query ID is required"
    assert candidate.product_id is not None, "Product ID is required"
    return True


def validate_ground_truth(gt: GroundTruth) -> bool:
    """Validate ground truth schema"""
    assert gt.query_id, "Query ID is required"
    assert gt.product_id is not None, "Product ID is required"
    assert gt.relevance in [0, 1, 2], "Relevance must be 0, 1, or 2"
    return True


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def save_schema(obj: Any, filepath: str) -> None:
    """Save schema object to JSON"""
    import json
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(obj.to_dict(), f, indent=2, ensure_ascii=False)


def load_schema(filepath: str, schema_class) -> Any:
    """Load schema object from JSON"""
    import json
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return schema_class.from_dict(data)


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":
    # Example: Create a product
    product = Product(
        id=1234,
        productDisplayName="Nike Air Max 90",
        masterCategory="Footwear",
        subCategory="Shoes",
        articleType="Sports Shoes",
        baseColour="White",
        gender="Men",
        season="Summer",
        year=2024,
        usage="Sports"
    )
    print("Product:", product.to_dict())
    
    # Example: Create a query
    query = QueryRecord(
        query_id="q001",
        query_text_original="Beyaz spor ayakkabı",
        query_text_tr="beyaz spor ayakkabı",
        query_norm=normalize_text("Beyaz spor ayakkabı", mode='aggressive'),
        intent=Intent.SEARCH,
        slots={"color": "white", "articleType": "shoes", "usage": "sports"}
    )
    print("Query:", query.to_dict())
    
    # Example: Create a candidate
    candidate = Candidate(
        query_id="q001",
        product_id=1234,
        text_score=0.85,
        image_score=0.92,
        hybrid_score=0.88,
        attr_matches={"color": True, "articleType": True}
    )
    print("Candidate:", candidate.to_dict())
