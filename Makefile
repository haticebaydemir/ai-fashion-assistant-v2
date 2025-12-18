# ========================================
# AI FASHION ASSISTANT V2.0 - MAKEFILE
# ========================================

.PHONY: help setup install clean test api ui demo docs

# Default target
help:
	@echo "AI Fashion Assistant v2.0 - Available Commands"
	@echo "=============================================="
	@echo "  make setup       - Initial project setup"
	@echo "  make install     - Install dependencies"
	@echo "  make clean       - Clean temporary files"
	@echo "  make test        - Run tests"
	@echo "  make api         - Start FastAPI server"
	@echo "  make ui          - Start Streamlit UI"
	@echo "  make demo        - Run end-to-end demo"
	@echo "  make docs        - Generate documentation"
	@echo "=============================================="

# Setup project
setup:
	@echo "🚀 Setting up AI Fashion Assistant v2.0..."
	@mkdir -p data/raw data/processed data/ground_truth data/schemas data/user_profiles
	@mkdir -p embeddings/text embeddings/image embeddings/hybrid embeddings/user
	@mkdir -p models/fusion models/reranker models/personalization models/checkpoints
	@mkdir -p indexes
	@mkdir -p configs
	@mkdir -p logs
	@mkdir -p docs/results
	@touch data/raw/.gitkeep
	@touch embeddings/text/.gitkeep
	@touch models/fusion/.gitkeep
	@touch indexes/.gitkeep
	@echo "✅ Project structure created!"
	@$(MAKE) install

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.log" -delete
	@echo "✅ Cleaned!"

# Run tests
test:
	@echo "🧪 Running tests..."
	@pytest tests/ -v --cov=src --cov-report=html
	@echo "✅ Tests completed!"

# Start API server
api:
	@echo "🚀 Starting FastAPI server..."
	@cd api && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start Streamlit UI
ui:
	@echo "🎨 Starting Streamlit UI..."
	@streamlit run ui/app.py --server.port 8501

# Run demo
demo:
	@echo "🎬 Running end-to-end demo..."
	@jupyter notebook notebooks/phase10_final/01_end_to_end_demo.ipynb

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation available in docs/"

# Development setup (with pre-commit hooks)
dev-setup: setup
	@echo "🛠️ Setting up development environment..."
	@pip install black flake8 mypy pre-commit
	@pre-commit install
	@echo "✅ Development environment ready!"

# Format code
format:
	@echo "🎨 Formatting code..."
	@black src/ api/ ui/ tests/
	@echo "✅ Code formatted!"

# Lint code
lint:
	@echo "🔍 Linting code..."
	@flake8 src/ api/ ui/ tests/ --max-line-length=100
	@mypy src/ --ignore-missing-imports
	@echo "✅ Linting completed!"

# Export requirements
freeze:
	@echo "📝 Exporting requirements..."
	@pip freeze > requirements_frozen.txt
	@echo "✅ Requirements exported to requirements_frozen.txt"

# Quick start (setup + demo)
quickstart: setup
	@echo "⚡ Quick start completed!"
	@echo "Next steps:"
	@echo "  1. Copy data to data/raw/"
	@echo "  2. Run: make demo"
