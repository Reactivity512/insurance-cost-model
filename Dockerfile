# Stage 1: Build
FROM python:3.14-slim AS builder

WORKDIR /app

# Установим сборочные зависимости только на этом этапе
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime (минимальный образ)
FROM python:3.14-slim

WORKDIR /app

# Копируем только установленные пакеты из builder
COPY --from=builder /install /usr/local

# Копируем приложение
COPY main.py .
COPY insurance_model_pipeline.joblib .

# Non-root пользователь
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]