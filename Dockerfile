# Use an official Python runtime as the parent image
FROM python:3.11-slim-bookworm

COPY requirements.txt requirements.txt
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
