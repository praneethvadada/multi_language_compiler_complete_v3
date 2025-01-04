# # Use Python 3.10 slim image
# FROM python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Copy the app files
# COPY . .

# # Install dependencies
# # RUN python3 -m venv /venv && \
# #     /venv/bin/pip install Flask requests flask-cors gunicorn uvicorn aiofiles
# RUN python3 -m venv /venv && \
#     /venv/bin/pip install Flask requests flask-cors gunicorn gevent

# # Expose the port Flask will run on
# EXPOSE 8080

# # Use gunicorn with uvicorn worker class for high concurrency
# # CMD ["/venv/bin/gunicorn", "-w", "8", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "app:app"]
# CMD ["/venv/bin/gunicorn", "-w", "8", "-k", "gevent", "--bind", "0.0.0.0:8080", "app:app"]

# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the app files
COPY . .

# Install dependencies including gevent
RUN python3 -m venv /venv && \
    /venv/bin/pip install Flask requests flask-cors gunicorn gevent

# Expose the port Flask will run on
EXPOSE 8080

# Use gunicorn with gevent for handling concurrent requests
CMD ["/venv/bin/gunicorn", "-w", "16", "-k", "gevent", "--bind", "0.0.0.0:8080", "app:app"]
