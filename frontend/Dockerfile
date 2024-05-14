FROM debian:latest
import m

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    nodejs \
    npm \
    curl \
    git && \
    npm install -g n && \
    n stable && \
    ln -sf /usr/local/bin/node /usr/bin/node && \
    ln -sf /usr/local/bin/npm /usr/bin/npm && \
    npm install --global yo generator-code

# Set the working directory inside the container
WORKDIR /workspace

# Keep the container running
CMD tail -f /dev/null
