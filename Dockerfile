# Dockerfile for Dortmund Property Monitor
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY dortmund_property_monitor.py .
COPY config.py .
COPY seen_properties.json .

# Create volume for persistent data
VOLUME ["/app/data"]

# Set environment variable for data directory
ENV DATA_DIR=/app/data

# Run the monitor
CMD ["python", "dortmund_property_monitor.py"]
