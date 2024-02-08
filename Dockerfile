#FROM python:3.11
#
#RUN curl -sSL https://pdm-project.org/install-pdm.py | python3 -
#ENV PATH=/root/.local/bin:$PATH
#
#RUN mkdir /booking
#WORKDIR /booking
#
#COPY pyproject.toml .
#COPY pdm.lock .
#RUN pdm install --prod
#
## ENV PYTHONPATH="${PYTHONPATH}:/booking/src"
#
#COPY . .
## RUN cp -r /booking/.venv/lib/python3.11/site-packages/sqladmin/statics/* /booking/static/
#
#RUN chmod a+x /booking/docker/*.sh
#
## CMD ["pdm", "run", "gunicorn", "main:create_app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]




ARG PYTHON_IMAGE=python:3.11.7-slim-bookworm

FROM $PYTHON_IMAGE as build

RUN pip install pdm
COPY ./pyproject.toml ./pdm.lock ./
RUN pdm export --prod -f requirements -o requirements.txt

FROM $PYTHON_IMAGE
ENV PYTHONPATH=$PYTHONPATH:/app/src \
    PATH=$PATH:/home/app/.local/bin \
    PYTHONUNBUFFERED=1

RUN addgroup --gid 2000 app && adduser --gid 2000 --uid 1000 app
USER app

WORKDIR /app

COPY --from=build ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user --no-dependencies

COPY ./src ./src
COPY alembic.ini ./
# COPY ./docker ./docker
# ENTRYPOINT ["uvicorn", "adapters.api.app:create_app", "--factory", "--loop", "uvloop", "--host", "0.0.0.0"]

# RUN chmod a+x ./app/docker/*.sh