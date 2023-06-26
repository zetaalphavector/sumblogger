#!/bin/bash
export PYTHONUNBUFFERED=0
uvicorn src.app:app --host 0.0.0.0 --port 8080 "$@"