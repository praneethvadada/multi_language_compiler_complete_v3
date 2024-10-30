FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install Flask
RUN python3 -m venv /venv && /venv/bin/pip install Flask requests flask-cors

# Use the virtual environment to run the app
CMD ["/venv/bin/python", "app.py"]
