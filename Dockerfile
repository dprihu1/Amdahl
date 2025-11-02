FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for matplotlib
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set Python to non-interactive mode for matplotlib
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

# Make cli.py executable
RUN chmod +x cli.py

# Default entrypoint
ENTRYPOINT ["python", "cli.py"]

