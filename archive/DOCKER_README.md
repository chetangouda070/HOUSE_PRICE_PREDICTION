# 🐳 Docker Deployment for Spam Detection API

## Why Docker?

Docker containers package your application and all its dependencies into a standardized unit that can run anywhere. Benefits for our spam detection API:

### ✅ **Advantages:**
- **Consistent Environment**: Same setup on dev, staging, production
- **Easy Deployment**: One command to run anywhere
- **Isolation**: No conflicts with system dependencies
- **Scalability**: Easy to run multiple instances
- **Version Control**: Track exact environment versions

### ❌ **When You Need Docker:**
- Deploying to cloud platforms (AWS, GCP, Azure)
- Team collaboration with consistent environments
- Running on different operating systems
- Production deployment with orchestration (Kubernetes)
- CI/CD pipelines

### ⚠️ **When Docker is Optional:**
- Local development only
- Single-user projects
- Learning/experimentation phase
- Simple deployments

## 🚀 Quick Start

### Prerequisites
```bash
# Install Docker Desktop: https://www.docker.com/products/docker-desktop
# Install Docker Compose: https://docs.docker.com/compose/install/
```

### Method 1: Docker Compose (Recommended)
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop
docker-compose down
```

### Method 2: Direct Docker Commands
```bash
# Build image
docker build -t spam-detection-api .

# Run container
docker run -p 8000:8000 --name spam-api spam-detection-api

# Stop and remove
docker stop spam-api
docker rm spam-api
```

### Method 3: Helper Script
```bash
# Make script executable (Windows PowerShell)
chmod +x docker-run.sh  # On Linux/Mac

# Build and run
./docker-run.sh compose-up

# Test API
./docker-run.sh test

# Clean up
./docker-run.sh clean
```

## 🧪 Testing Your Containerized API

Once running, test the API:

```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"message": "WIN a FREE iPhone!"}'

# Batch prediction
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '["Hello!", "FREE prize!"]'
```

## 📁 Project Structure for Docker

```
spam-detection-project/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container setup
├── .dockerignore          # Files to exclude from build
├── docker-run.sh          # Helper script
├── requirements.txt        # Python dependencies
├── app.py                  # FastAPI application
├── spam_classifier.pkl     # Trained model
├── model_metadata.pkl      # Model information
└── README.md              # This file
```

## 🔧 Docker Configuration Explained

### Dockerfile Breakdown:
```dockerfile
FROM python:3.9-slim          # Lightweight Python base image
WORKDIR /app                  # Set working directory
COPY requirements.txt .       # Copy dependencies first (caching)
RUN pip install -r requirements.txt  # Install Python packages
COPY app.py model_files .     # Copy application code
EXPOSE 8000                   # Expose port 8000
CMD ["uvicorn", "app:app"]    # Run the application
```

### Key Optimizations:
- **Multi-stage builds**: Smaller final image
- **Dependency caching**: Faster rebuilds
- **Security**: Non-root user
- **Health checks**: Automatic monitoring

## 🌐 Production Deployment

### Cloud Platforms:
```bash
# AWS ECR + ECS/Fargate
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag spam-detection-api:latest <account>.dkr.ecr.<region>.amazonaws.com/spam-api:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/spam-api:latest

# Google Cloud Run
gcloud builds submit --tag gcr.io/<project>/spam-api
gcloud run deploy --image gcr.io/<project>/spam-api --platform managed

# Azure Container Instances
az container create --resource-group <rg> --name spam-api --image <registry>/spam-api --ports 8000
```

### Kubernetes:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spam-detection-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: spam-api
  template:
    metadata:
      labels:
        app: spam-api
    spec:
      containers:
      - name: api
        image: spam-detection-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## 🔍 Troubleshooting

### Common Issues:

**Port already in use:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill process or change port
docker run -p 8001:8000 spam-detection-api
```

**Model loading errors:**
```bash
# Check if model files exist in container
docker run -it spam-detection-api ls -la

# Check Python path
docker run -it spam-detection-api python -c "import joblib; print(joblib.__version__)"
```

**Memory issues:**
```bash
# Increase Docker memory limit in Docker Desktop settings
# Or add memory limits to docker-compose.yml
```

## 📊 Performance Comparison

| Method | Startup Time | Memory Usage | Portability | Production Ready |
|--------|-------------|--------------|-------------|------------------|
| Local Python | Instant | Variable | ❌ | ❌ |
| Docker | 10-30s | Consistent | ✅ | ✅ |
| Cloud Deploy | 30-60s | Scalable | ✅ | ✅ |

## 🎯 When to Use Docker vs. Not

### ✅ **Use Docker When:**
- Multiple developers on different OS
- Deploying to cloud platforms
- Need consistent environments
- Running multiple services
- CI/CD pipelines
- Production deployments

### ❌ **Skip Docker When:**
- Learning/experimenting locally
- Simple single-user projects
- No deployment plans
- Time constraints for learning
- Very simple applications

## 🚀 Next Steps

1. **Try it locally first:**
   ```bash
   docker-compose up --build
   ```

2. **Test thoroughly:**
   ```bash
   ./docker-run.sh test
   ```

3. **Deploy to cloud:**
   - Push to container registry
   - Deploy to your preferred platform
   - Set up monitoring and scaling

4. **Learn more:**
   - Docker documentation: https://docs.docker.com/
   - Kubernetes for orchestration: https://kubernetes.io/

---

**Bottom Line:** Docker is **highly recommended** for production ML deployments, but **optional** for local development and learning. Start with docker-compose for easy testing! 🐳