FROM python:3.13.1 AS base


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ENV POETRY_VERSION=2.0.0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME='/usr/local' \
    PATH="/root/.local/bin:$PATH"

RUN python3 -m pip install --no-cache-dir --upgrade pip pipx \
    && python3 -m pipx ensurepath \
    && pipx install poetry==$POETRY_VERSION

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

RUN ln -sf /usr/local/bin/python3 /usr/bin/python3.13  \
    && poetry install --no-interaction --no-ansi --no-root \
    && apt-get update && apt-get install -y netcat-traditional

FROM base as development


COPY ./entrypoint.sh ./

RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]

COPY . .
