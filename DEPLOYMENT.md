# Traffic App Deployment Guide

## Quick Start

To deploy the traffic_app in production mode:

```bash
docker-compose up -d
```

## What This Sets Up

1. **Flask Application**: Runs on Gunicorn with 4 workers
2. **Nginx Reverse Proxy**: Handles requests on port 80
3. **Production Configuration**: Optimized for performance and security

## Services

- **flask_app**: Your Flask application running on internal port 8000
- **nginx**: Reverse proxy exposing the app on port 80

## Health Checks

- Application health: `http://localhost/health`
- Nginx health: Built-in health checks

## Useful Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Check service status
docker-compose ps
```

## Testing the API

```bash
# Test health endpoint
curl http://localhost/health

# Test prediction endpoint
curl -X POST http://localhost/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]}'
```

## Dependencies Included

The requirements.txt now includes all necessary packages:
- **Flask 2.3.3** - Web framework
- **XGBoost 2.1.4** - Machine learning model (your traffic_model.pkl uses this)
- **pandas 2.0.3** - Data manipulation
- **scikit-learn 1.3.0** - ML utilities
- **numpy 1.24.3** - Numerical computing
- **joblib 1.3.2** - Model serialization
- **flask-cors 4.0.0** - CORS support
- **gunicorn 21.2.0** - Production WSGI server

## Configuration

- **Python Version**: 3.11.9 (matches your environment)
- **Dependencies**: Exact versions from requirements.txt (including XGBoost)
- **Workers**: 4 Gunicorn workers
- **Timeout**: 120 seconds
- **Port**: 80 (external), 8000 (internal Flask app)