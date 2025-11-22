FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.path --unset
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .
RUN poetry install

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
