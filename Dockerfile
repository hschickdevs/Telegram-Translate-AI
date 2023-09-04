# Docker image location:
# https://hub.docker.com/repository/docker/hschickdevs/telegram-translate-ai/general

# Image URL for GCP Compute:
# hschickdevs/telegram-translate-ai:latest

# How to install docker engine on Ubuntu:
# https://docs.docker.com/engine/install/ubuntu/ 

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
# Ensure that readme is included for docker hub
COPY README.md /app/README.md

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the bot when the container launches
CMD ["python3", "-m", "src"]

# ------- Docker Deployment Commands: -------
# docker build -t translate-bot .
# docker run --env-file .env bot
# docker tag translate-bot hschickdevs/telegram-translate-ai:latest
# docker push hschickdevs/telegram-translate-ai:latest