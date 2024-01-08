FROM python:3.11

RUN mkdir /booking

WORKDIR /booking

COPY pyproject.toml .
COPY pdm.lock .

RUN pip install pdm
RUN pdm install --prod

COPY . .

CMD ["pdm", "run", "gunicorn", "main:create_app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]