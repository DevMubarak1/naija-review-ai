#!/bin/bash
echo "Starting NaijaReview AI..."

# Start FastAPI in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait for API to start
sleep 5

# Start Streamlit
streamlit run app/streamlit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true &
UI_PID=$!

echo "API running on :8000, UI running on :8501"

# Wait for either process to exit
wait -n $API_PID $UI_PID
