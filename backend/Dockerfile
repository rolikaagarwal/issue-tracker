FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY backend/pyproject.toml backend/poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

COPY backend/ ./

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
