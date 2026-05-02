#!/bin/bash
# Start FastAPI on a fixed internal port (not exposed externally)
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on Heroku's dynamically assigned port
streamlit run ui/care_gap_app.py \
    --server.port "$PORT" \
    --server.address 0.0.0.0 \
    --server.headless true
