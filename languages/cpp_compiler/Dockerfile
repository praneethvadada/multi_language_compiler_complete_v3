FROM gcc:latest

WORKDIR /app
COPY . .

# Install Python and pip dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment and install Flask in it
RUN python3 -m venv /venv && /venv/bin/pip install Flask

# Use the virtual environment to run the app
CMD ["/venv/bin/python", "app.py"]
