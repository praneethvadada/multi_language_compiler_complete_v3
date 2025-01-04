# Use OpenJDK 17 slim image
FROM openjdk:17-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python and Flask
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install Flask flask-cors && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose port for the Flask application
EXPOSE 8080

# Run the Flask app
CMD ["python3", "app.py"]

# # Use OpenJDK 17 slim image
# FROM openjdk:17-slim

# # Set working directory
# WORKDIR /app

# # Copy application files
# COPY . .

# # Install dependencies (if any additional are required)
# RUN apt-get update && apt-get install -y \
#     curl \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# # Expose port for Flask application
# EXPOSE 8080

# # Run the Flask app
# CMD ["java", "-cp", "app.jar", "Main"]

# # # Use OpenJDK base image
# # FROM openjdk:11-jdk-slim

# # # Set working directory
# # WORKDIR /app

# # # Install Python and necessary dependencies
# # RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# # # Create Python virtual environment and install Flask
# # RUN python3 -m venv /venv && /venv/bin/pip install Flask flask-cors

# # # Copy application files into the container
# # COPY . .

# # # Expose port for Flask application
# # EXPOSE 8080

# # # Command to start the Flask server
# # CMD ["/venv/bin/python", "app.py"]



# # # FROM openjdk:11-jdk-slim

# # # WORKDIR /app
# # # COPY . .

# # # # Install Python and pip dependencies
# # # RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# # # # Create a virtual environment and install Flask in it
# # # # RUN python3 -m venv /venv && /venv/bin/pip install Flask
# # # RUN python3 -m venv /venv && /venv/bin/pip install Flask requests flask-cors

# # # # Use the virtual environment to run the app
# # # CMD ["/venv/bin/python", "app.py"]
