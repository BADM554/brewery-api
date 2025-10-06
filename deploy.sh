#!/bin/bash
# Quick deployment script for Hetzner VPS

set -e

echo "==================================="
echo "Brewery API - Hetzner Deployment"
echo "==================================="
echo ""

# Check if SERVER_IP is provided
if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh SERVER_IP"
    echo "Example: ./deploy.sh 123.45.67.89"
    exit 1
fi

SERVER_IP=$1
DEPLOY_PATH="/opt/badm554-api"

echo "Deploying to: $SERVER_IP"
echo ""

# Create deployment directory on server
echo "1. Creating deployment directory..."
ssh root@$SERVER_IP "mkdir -p $DEPLOY_PATH"

# Copy files to server
echo "2. Copying files to server..."
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' \
    ./ root@$SERVER_IP:$DEPLOY_PATH/

# Deploy with Docker
echo "3. Starting Docker containers..."
ssh root@$SERVER_IP << 'ENDSSH'
cd /opt/badm554-api
docker-compose down
docker-compose up -d --build
echo ""
echo "Waiting for containers to start..."
sleep 5
docker-compose ps
echo ""
echo "Testing API..."
curl -s http://localhost:8000/health | jq || echo "API health check failed"
ENDSSH

echo ""
echo "==================================="
echo "Deployment Complete!"
echo "==================================="
echo ""
echo "API URL: http://$SERVER_IP:8000"
echo ""
echo "Test with:"
echo "  curl http://$SERVER_IP:8000/"
echo ""
echo "View logs:"
echo "  ssh root@$SERVER_IP 'cd /opt/badm554-api && docker-compose logs -f'"
echo ""
