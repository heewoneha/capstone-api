FROM python:3.10-slim

RUN addgroup --gid 1000 user
RUN adduser --disabled-password --gecos '' --uid 1000 --gid 1000 user

RUN apt-get update && apt-get install -y \
    curl build-essential git libgl1 libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ARG POETRY_VERSION=1.8.5
ARG POETRY_HOME=/opt/poetry
RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION &&\
    $POETRY_HOME/bin/poetry --version
ENV PATH="$PATH:${POETRY_HOME}/bin"


WORKDIR /code

RUN mkdir -p ./app/services/tmp_model_sources/character \
    ./app/services/tmp_model_sources/background \
    ./app/services/tmp_model_results && \
    chown -R user:user /code/app/services/tmp_model_sources \
    && chown -R user:user /code/app/services/tmp_model_results

USER user

WORKDIR /code

ENV PYTHONPATH=/code
ENV CAPSTONE_API_SCRIPT_PATH=/code
ENV PYOPENGL_PLATFORM=osmesa

COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock
RUN poetry install


COPY . /code

CMD ["poetry", "run", "gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "120"]
