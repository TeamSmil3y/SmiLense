# Use the official Debian slim image as the base
FROM debian:stable-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3.11-venv

# Set the working directory in the container
WORKDIR /app

# Keep the container running
CMD tail -f /dev/null
