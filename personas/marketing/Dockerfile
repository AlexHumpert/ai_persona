FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cache utilization
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application directory
COPY . .

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port 8080 - Cloud Run will use this
EXPOSE 8080

# Command to run the application
CMD ["streamlit", "run", "main.py"]