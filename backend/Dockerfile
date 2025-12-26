# ------------ STAGE 1: Build ------------
FROM python:3.10-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ------------ STAGE 2: Runtime ------------
FROM python:3.10-slim

# Create non-root user
RUN adduser --disabled-password appuser
USER appuser

WORKDIR /app

# Copy installed packages into location accessible to non-root user
COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
