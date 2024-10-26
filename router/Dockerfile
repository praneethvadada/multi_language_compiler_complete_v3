FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install Flask and requests in a virtual environment
RUN python3 -m venv /venv && /venv/bin/pip install Flask requests

# Use the virtual environment to run the router
CMD ["/venv/bin/python", "router.py"]
