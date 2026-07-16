FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_WEIGHTS_PATH=/app/weights/best_model.pth

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src /app/src
COPY weights /app/weights

# Create outputs directory for GradCAM results
RUN mkdir -p /app/outputs

# Expose port
EXPOSE 8000

# Start server using production uvicorn settings
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
