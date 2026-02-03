FROM python:3.12.2-slim-bullseye

# Security best practices
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install jq
RUN apt-get update && apt-get install -y --no-install-recommends jq \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with its home directory
RUN useradd --create-home pythonuser

# Create /code directory and set ownership before switching user
RUN mkdir -p /code && chown pythonuser:pythonuser /code

USER pythonuser
WORKDIR /code

# Optional: Only if you have specific dependencies
# COPY --chown=appuser:appuser requirements.txt .
RUN pip install claude-agent-sdk
