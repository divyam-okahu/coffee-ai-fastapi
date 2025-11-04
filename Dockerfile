FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy .env file if it exists
COPY .env* ./

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "app.py"]
