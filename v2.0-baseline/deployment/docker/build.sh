#!/bin/bash
# Build Docker image

set -e

echo "🐳 Building Docker image..."

# Build
docker build -f docker/Dockerfile -t fashion-api:latest .

echo "✅ Build complete!"
echo "📊 Image size:"
docker images fashion-api:latest
