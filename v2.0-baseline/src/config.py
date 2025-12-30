"""
Configuration Management
========================

Centralized configuration for all project settings.

Author: AI Fashion Assistant Team
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import os
from dataclasses import dataclass, field


# ============================================================
# BASE PATHS
# ============================================================

# Project root (adjust based on execution context)
if 'COLAB_GPU' in os.environ or 'google.colab' in str(get_ipython()):
    # Running in Colab
    PROJECT_ROOT = Path("/content/drive/MyDrive/ai_fashion_assistant_v2")
else:
    # Running locally
    PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
GT_DATA_DIR = DATA_DIR / "ground_truth"
SCHEMA_DIR = DATA_DIR / "schemas"
USER_DATA_DIR = DATA_DIR / "user_profiles"

# Embedding directories
EMB_DIR = PROJECT_ROOT / "embeddings"
TEXT_EMB_DIR = EMB_DIR / "text"
IMAGE_EMB_DIR = EMB_DIR / "image"
HYBRID_EMB_DIR = EMB_DIR / "hybrid"
USER_EMB_DIR = EMB_DIR / "user"

# Model directories
MODELS_DIR = PROJECT_ROOT / "models"
FUSION_DIR = MODELS_DIR / "fusion"
RERANKER_DIR = MODELS_DIR / "reranker"
PERSONALIZATION_DIR = MODELS_DIR / "personalization"
CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"

# Index directories
INDEXES_DIR = PROJECT_ROOT / "indexes"

# Config directory
CONFIGS_DIR = PROJECT_ROOT / "configs"


# ============================================================
# MODEL CONFIGURATIONS
# ============================================================

@dataclass
class ModelConfig:
    """Model configuration"""
    
    # Text models
    text_model_primary: str = "paraphrase-multilingual-mpnet-base-v2"
    text_model_primary_dim: int = 768
    
    text_model_secondary: str = "openai/clip-vit-large-patch14"  # text encoder
    text_model_secondary_dim: int = 512
    
    # Image model
    image_model: str = "openai/clip-vit-large-patch14"
    image_model_dim: int = 768
    
    # Derived dimensions
    @property
    def text_combined_dim(self) -> int:
        return self.text_model_primary_dim + self.text_model_secondary_dim
    
    @property
    def hybrid_dim(self) -> int:
        return self.text_combined_dim + self.image_model_dim
    
    # LLM
    llm_provider: str = "openai"  # or "anthropic", "local"
    llm_model: str = "gpt-3.5-turbo"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    
    # Device
    device: str = "cuda"  # or "cpu"
    batch_size_text: int = 128
    batch_size_image: int = 64


@dataclass
class RetrievalConfig:
    """Retrieval configuration"""
    
    # FAISS
    faiss_index_type: str = "HNSW"  # or "Flat", "IVF"
    faiss_m: int = 32
    faiss_ef_construction: int = 200
    faiss_ef_search: int = 128
    
    # Search
    default_top_k: int = 10
    max_top_k: int = 100
    
    # Hybrid search
    default_alpha: float = 0.5  # text weight
    alpha_range: tuple = (0.0, 1.0)
    
    # Query rewriting
    enable_rewrite: bool = True
    num_rewrites: int = 3
    rewrite_merge_strategy: str = "union"  # or "weighted"


@dataclass
class RankingConfig:
    """Ranking configuration"""
    
    # Phase G (Learned Fusion)
    fusion_model_type: str = "lightgbm"  # or "xgboost"
    fusion_features: list = field(default_factory=lambda: [
        "text_score", "image_score",
        "text_rank", "image_rank",
        "category_match", "color_match", "gender_match",
        "cross_modal_score", "price_similarity"
    ])
    
    # Phase H (Attribute-Aware)
    attr_rerank_mode: str = "soft"  # or "hard"
    attr_boost_weights: Dict[str, float] = field(default_factory=lambda: {
        "color": 0.20,
        "gender": 0.15,
        "category": 0.10,
        "articleType": 0.10,
        "usage": 0.05
    })
    
    # Confidence threshold for hard constraints
    confidence_threshold: float = 0.8
    
    # Personalization
    personalization_weight: float = 0.3


@dataclass
class EvaluationConfig:
    """Evaluation configuration"""
    
    # Metrics
    metrics: list = field(default_factory=lambda: [
        "hit@1", "hit@3", "hit@5", "hit@10",
        "mrr", "map", "ndcg@5", "ndcg@10"
    ])
    
    # Test set
    test_size: int = 1000
    test_random_seed: int = 42
    stratify_by: str = "masterCategory"
    
    # Ablation
    ablation_components: list = field(default_factory=lambda: [
        "baseline",
        "rewrite",
        "fusion",
        "attribute_soft",
        "attribute_hard",
        "personalization"
    ])


@dataclass
class APIConfig:
    """API configuration"""
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # CORS
    cors_origins: list = field(default_factory=lambda: ["*"])
    
    # Rate limiting
    rate_limit: int = 10  # requests per minute
    
    # Caching
    enable_cache: bool = True
    cache_ttl: int = 3600  # seconds
    
    # Logging
    log_level: str = "INFO"


# ============================================================
# MAIN CONFIG CLASS
# ============================================================

@dataclass
class Config:
    """Main configuration class"""
    
    model: ModelConfig = field(default_factory=ModelConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    ranking: RankingConfig = field(default_factory=RankingConfig)
    evaluation: EvaluationConfig = field(default_factory=EvaluationConfig)
    api: APIConfig = field(default_factory=APIConfig)
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'Config':
        """Load configuration from YAML file"""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return cls(
            model=ModelConfig(**data.get('model', {})),
            retrieval=RetrievalConfig(**data.get('retrieval', {})),
            ranking=RankingConfig(**data.get('ranking', {})),
            evaluation=EvaluationConfig(**data.get('evaluation', {})),
            api=APIConfig(**data.get('api', {}))
        )
    
    def to_yaml(self, yaml_path: Path) -> None:
        """Save configuration to YAML file"""
        import dataclasses
        
        data = {
            'model': dataclasses.asdict(self.model),
            'retrieval': dataclasses.asdict(self.retrieval),
            'ranking': dataclasses.asdict(self.ranking),
            'evaluation': dataclasses.asdict(self.evaluation),
            'api': dataclasses.asdict(self.api)
        }
        
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)


# ============================================================
# SINGLETON CONFIG INSTANCE
# ============================================================

# Default config
_config = Config()

def get_config() -> Config:
    """Get global config instance"""
    return _config

def set_config(config: Config) -> None:
    """Set global config instance"""
    global _config
    _config = config

def load_config_from_file(yaml_path: Path) -> Config:
    """Load config from YAML and set as global"""
    config = Config.from_yaml(yaml_path)
    set_config(config)
    return config


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

def load_env_vars() -> Dict[str, str]:
    """Load environment variables"""
    from dotenv import load_dotenv
    
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
        "HF_TOKEN": os.getenv("HF_TOKEN", ""),
    }


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def ensure_directories() -> None:
    """Create all necessary directories"""
    dirs = [
        DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, GT_DATA_DIR, SCHEMA_DIR, USER_DATA_DIR,
        EMB_DIR, TEXT_EMB_DIR, IMAGE_EMB_DIR, HYBRID_EMB_DIR, USER_EMB_DIR,
        MODELS_DIR, FUSION_DIR, RERANKER_DIR, PERSONALIZATION_DIR, CHECKPOINTS_DIR,
        INDEXES_DIR, CONFIGS_DIR
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


def print_config(config: Optional[Config] = None) -> None:
    """Print configuration"""
    if config is None:
        config = get_config()
    
    print("=" * 60)
    print("CONFIGURATION")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Text Model: {config.model.text_model_primary}")
    print(f"Image Model: {config.model.image_model}")
    print(f"LLM Model: {config.model.llm_model}")
    print(f"Hybrid Dim: {config.model.hybrid_dim}")
    print(f"Default Top-K: {config.retrieval.default_top_k}")
    print(f"Default Alpha: {config.retrieval.default_alpha}")
    print("=" * 60)


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":
    # Create default config
    config = Config()
    
    # Print config
    print_config(config)
    
    # Save to YAML
    config.to_yaml(CONFIGS_DIR / "config.yaml")
    print(f"Config saved to {CONFIGS_DIR / 'config.yaml'}")
    
    # Load from YAML
    loaded_config = Config.from_yaml(CONFIGS_DIR / "config.yaml")
    print("Config loaded successfully!")
    
    # Ensure directories exist
    ensure_directories()
    print("All directories created!")
