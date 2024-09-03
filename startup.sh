#!/bin/sh

# set -e 

gunicorn main:app --preload --workers 2 --threads 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 --timeout 3600