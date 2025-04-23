# =============================================================================
# EquityLens - API Service Dockerfile
# =============================================================================
# This Dockerfile builds the FastAPI service that provides REST endpoints
# for accessing portfolio analytics, risk metrics, and financial data.
# =============================================================================

# Use specific Python version for stability and reproducibility
FROM python:3.10-slim

# Set working directory for all subsequent commands
WORKDIR /app

# Copy requirements first to leverage Docker's build cache
COPY requirements.txt .

# Install system dependencies for certain Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Command to run the API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Metadata about the image
LABEL maintainer="EquityLens Team" \
      version="0.1.0" \
      description="FastAPI service for portfolio analytics and risk management"