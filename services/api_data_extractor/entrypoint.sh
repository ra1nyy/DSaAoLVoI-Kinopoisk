python -m uvicorn main:app --host 0.0.0.0 --port "$UVICORN_SERVER_PORT" --root-path "$API_PREFIX" --workers "$WORKERS_COUNT"
