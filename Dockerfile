# Use a slim Python base image for efficiency and smaller image size
FROM python:3.10-slim-buster

# Set environment variables:
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Collect static files during the image build process
RUN python manage.py collectstatic --no-input

# Expose the port Gunicorn will listen on
EXPOSE 8000 # CraftDoc uses 8000

# Command to run the Gunicorn server when the container starts.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "adminlte2.wsgi:application"] # Correct for CraftDoc