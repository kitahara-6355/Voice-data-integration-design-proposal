# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies that might be needed by libraries like av (for ffmpeg)
# This is good practice for a robust image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY ./app ./app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run the app.
# We run from the /code directory where the `app` package is.
# The host must be 0.0.0.0 to be reachable from outside the container.
# Using --loop asyncio as we determined it was more stable in the environment.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio"]
