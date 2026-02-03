FROM python:3.12-slim-bookworm

# Security best practices
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_RETRIES=5

# Install jq and ensure CA certs are up to date (helps with SSL to PyPI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Install Python deps as root so site-packages is writeable; avoids SSL issues from user install path
RUN pip install --no-cache-dir claude-agent-sdk

# Create a non-root user with its home directory
RUN useradd --create-home pythonuser

# Create /code directory and set ownership before switching user
RUN mkdir -p /code && chown pythonuser:pythonuser /code

USER pythonuser
WORKDIR /code
