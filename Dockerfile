# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/code/src
# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Disable Poetry's virtual environment as Docker provides isolation
RUN poetry config virtualenvs.create false

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* /code/

# Install dependencies without creating a virtual environment
RUN poetry install --no-interaction --no-ansi

# Copy project
COPY src/ /code/src

# Make the entrypoint script executable
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Command to run the Gunicorn server
ENTRYPOINT ["/code/entrypoint.sh"]
