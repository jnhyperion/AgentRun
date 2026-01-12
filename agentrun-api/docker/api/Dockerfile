FROM python:3.12.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /code

# Copy the agentrun package first (for -e .. in requirements.txt)
COPY ./agentrun /code/agentrun
COPY ./pyproject.toml /code/

# Install dependencies
COPY ./agentrun-api/requirements.txt /code/agentrun-api/
RUN pip install -r agentrun-api/requirements.txt

# Copy the API source
COPY ./agentrun-api/src /code/