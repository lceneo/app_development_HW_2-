FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.path --unset
RUN poetry config virtualenvs.in-project true

# Копируем только конфиги
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости + проект (проект ещё НЕ скопирован, но package-mode позволит)
RUN poetry install --no-root

# Теперь копируем исходники пакета
COPY . .
# Устанавливаем проект (теперь папка app существует)
RUN poetry install

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
