# GCP Cloud Run Deployment Guide

## Prerequisites
- gcloud CLI installed and configured
- Docker image built

## Steps

### 1. Build and Push to GCR
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Tag image
docker tag fashion-api:latest gcr.io/<project-id>/fashion-api:latest

# Push
docker push gcr.io/<project-id>/fashion-api:latest
```

### 2. Deploy to Cloud Run
```bash
gcloud run deploy fashion-api \
  --image gcr.io/<project-id>/fashion-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --port 8000
```

### 3. Get Service URL
```bash
gcloud run services describe fashion-api --region us-central1 --format="value(status.url)"
```

## Estimated Cost
- Cloud Run (pay per use): $0.00002400 per vCPU-second
- Request: $0.40 per million requests
- Estimate: $20-50/month (moderate traffic)
