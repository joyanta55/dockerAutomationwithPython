FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Docker inside the container
RUN apt-get update && apt-get install -y \
    curl \
    lsb-release \
    gnupg2 \
    ca-certificates \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y docker-ce-cli

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application when the container starts
CMD ["python", "main.py"]
