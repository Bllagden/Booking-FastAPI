#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    pdm run celery --app=src.tasks.celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    pdm run celery --app=src.tasks.celery:celery flower --url_prefix=/flower
fi