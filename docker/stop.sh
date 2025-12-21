#!/bin/bash
# Stop all services

set -e

echo "🛑 Stopping services..."

cd docker
docker-compose down

echo "✅ All services stopped!"
