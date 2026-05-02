import os

# On Heroku: set API_URL env var if backend is deployed separately.
# Default works for single-dyno setup where FastAPI runs on port 8000 internally.
API_URL = os.getenv("API_URL", "http://localhost:8000")
