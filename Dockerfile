# Dockerfile for Production Build
# Use the official Python 3.13 image as the base image.
FROM python:3.13

# Set the working directory in the container.
WORKDIR /app

# Copy requirements file to the container.
# This file should list all Python dependencies.
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code.
COPY . /app

# Expose port 8080 which uvicorn will run on.
EXPOSE 8080

# Command to run FastAPI in production mode using uvicorn.
# Explanation:
# - "main:app": refers to the 'app' in main.py.
# - "--host 0.0.0.0": makes the app accessible externally.
# - "--port 8080": serves the app on port 8080.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
