#!/bin/bash
# Deploy with Docker Compose

set -e

echo "🚀 Deploying services..."

cd docker

# Stop existing
docker-compose down

# Start services
docker-compose up -d

echo "✅ Deployment complete!"
echo "📊 Services:"
docker-compose ps

echo ""
echo "🌐 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "💚 Health: http://localhost:8000/api/v1/health"
