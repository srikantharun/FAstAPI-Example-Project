FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
# Pin urllib3 to specific version for compatibility
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/app/templates/reports
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]