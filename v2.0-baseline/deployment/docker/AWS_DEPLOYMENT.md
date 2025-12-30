# AWS ECS Deployment Guide

## Prerequisites
- AWS CLI installed and configured
- Docker image built and pushed to ECR

## Steps

### 1. Create ECR Repository
```bash
aws ecr create-repository --repository-name fashion-api
```

### 2. Build and Push Image
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag fashion-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/fashion-api:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/fashion-api:latest
```

### 3. Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name fashion-cluster
```

### 4. Create Task Definition
See `ecs-task-definition.json`

### 5. Create Service
```bash
aws ecs create-service \
  --cluster fashion-cluster \
  --service-name fashion-api-service \
  --task-definition fashion-api-task \
  --desired-count 2 \
  --launch-type FARGATE
```

## Estimated Cost
- Fargate (2 tasks, 0.5 vCPU, 1GB): ~$30/month
- Application Load Balancer: ~$16/month
- Total: ~$50/month
