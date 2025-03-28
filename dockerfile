FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    findutils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make scripts executable
RUN chmod +x setup.sh docker-entrypoint.sh

# Run debug script to help diagnose issues
RUN python debug_setup.py

# Set up the entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"