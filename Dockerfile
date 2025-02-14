FROM python:3.12.3-slim

# Set environment variables
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONUNBUFFERED=1

# Install uv
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip uv && uv venv recreate

# Set entrypoint
CMD ["uvicorn", "src.main:app", "--host 0.0.0.0", "--port 8000"]