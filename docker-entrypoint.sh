#!/bin/bash
set -e

echo "==== STARTING SERVER ===="
# Start the API server
exec uvicorn app:app --host 0.0.0.0 --port 7860