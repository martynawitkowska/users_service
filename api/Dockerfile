FROM python:3.13.1 AS development


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ENV POETRY_VERSION=2.0.0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME='/usr/local' \
    PATH="/root/.local/bin:$PATH"

RUN python3 -m pip install --no-cache-dir --upgrade pip pipx \
    && python3 -m pipx ensurepath

RUN pipx install poetry==$POETRY_VERSION

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root

RUN apt-get update && apt-get install -y netcat-traditional

COPY ./entrypoint.sh ./

RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]

COPY . .

FROM development as prod

COPY --from=development /app /app

RUN poetry install --without dev --sync