# Use a lightweight base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Update
RUN apt-get update -y
RUN apt-get upgrade -y
RUN python3 -m pip install --upgrade pip

# Install dependencies
RUN apt-get install -y libpq-dev gcc
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5150

# Define the command to run the application
CMD ["python", "app.py"]
