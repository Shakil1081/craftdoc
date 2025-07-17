FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies for psycopg2, mysqlclient, weasyprint, pycairo
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    python3-dev \
    libcairo2-dev \
    pango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libxml2 \
    libxml2-dev \
    libxslt1-dev \
    wkhtmltopdf \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional)
# RUN python manage.py collectstatic --no-input

# Expose port (Gunicorn default or whatever you use)
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "yourproject.wsgi:application"]
