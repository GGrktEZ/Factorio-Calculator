# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY data/ ./data/
COPY Main.py .

# Create output directories
RUN mkdir -p "calculation trees"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color

# Default command - run in wizard mode
CMD ["python", "Main.py"]
