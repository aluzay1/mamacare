FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    curl \
    netcat-openbsd \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install numpy and pandas first with specific versions
RUN pip install --no-cache-dir numpy==1.21.6 && \
    pip install --no-cache-dir pandas==1.3.5 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create a script to wait for PostgreSQL
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Create startup script
COPY startup.py /startup.py
RUN chmod +x /startup.py

# Create a startup wrapper script
RUN echo '#!/bin/bash\n\
/wait-for-postgres.sh db\n\
python /startup.py\n\
flask run --host=0.0.0.0 --port=5000' > /start.sh && chmod +x /start.sh

# Run the application with startup script
CMD ["/start.sh"] 