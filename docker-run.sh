#!/bin/bash

# Docker Helper Script for Spam Detection API
# ===========================================

echo "🐳 Spam Detection API - Docker Helper"
echo "====================================="

case "$1" in
    "build")
        echo "🏗️  Building Docker image..."
        docker build -t spam-detection-api .
        ;;

    "run")
        echo "🚀 Running container..."
        docker run -p 8000:8000 --name spam-api spam-detection-api
        ;;

    "compose-up")
        echo "🚀 Starting with docker-compose..."
        docker-compose up --build
        ;;

    "compose-down")
        echo "🛑 Stopping containers..."
        docker-compose down
        ;;

    "test")
        echo "🧪 Testing API..."
        sleep 5  # Wait for container to start
        curl -X GET "http://localhost:8000/health"
        echo -e "\n"
        curl -X POST "http://localhost:8000/predict" \
             -H "Content-Type: application/json" \
             -d '{"message": "WIN a FREE iPhone!"}'
        ;;

    "logs")
        echo "📋 Showing container logs..."
        docker logs spam-api
        ;;

    "clean")
        echo "🧹 Cleaning up..."
        docker stop spam-api 2>/dev/null || true
        docker rm spam-api 2>/dev/null || true
        docker rmi spam-detection-api 2>/dev/null || true
        ;;

    "help"|*)
        echo "Usage: $0 {build|run|compose-up|compose-down|test|logs|clean|help}"
        echo ""
        echo "Commands:"
        echo "  build       - Build Docker image"
        echo "  run         - Run container directly"
        echo "  compose-up  - Start with docker-compose"
        echo "  compose-down- Stop containers"
        echo "  test        - Test the running API"
        echo "  logs        - Show container logs"
        echo "  clean       - Remove containers and images"
        echo "  help        - Show this help"
        ;;
esac