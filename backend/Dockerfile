# ------------ STAGE 1: Build ------------
FROM python:3.10-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt


# ------------ STAGE 2: Runtime ------------
FROM python:3.10-slim

# Install curl for HEALTHCHECK
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password appuser

WORKDIR /app

# Copy installed Python packages
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Switch to non-root user
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -f http://localhost:5000/health || exit 1
