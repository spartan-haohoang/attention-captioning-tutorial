# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Copy dependency files
COPY requirements.txt requirements-dev.txt ./
COPY pyproject.toml ./

# Install Python dependencies
RUN uv pip install --system -r requirements.txt
RUN uv pip install --system -r requirements-dev.txt

# Install Jupyter and extensions
RUN uv pip install --system \
    jupyter \
    jupyterlab \
    ipywidgets \
    nbconvert

# Create directories for data and notebooks
RUN mkdir -p /app/data /app/notebooks /app/models

# Copy project files
COPY . /app/

# Expose Jupyter port
EXPOSE 8888

# Create a non-root user
RUN useradd --create-home --shell /bin/bash jupyter && \
    chown -R jupyter:jupyter /app
USER jupyter

# Set default command to start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
