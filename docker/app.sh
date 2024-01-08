#!/bin/bash

alembic upgrade head

pdm run gunicorn main:create_app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000