# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents (your project files) into the container
COPY . .

# Set the FLASK_APP environment variable to the file containing the app
ENV FLASK_APP=flask_app.py

# Make port 5000 available to the world outside the container
EXPOSE 5000

# Define the command to run your app using flask
CMD ["flask", "run", "--host=0.0.0.0"]
