
# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install netcat for the wait-for-db script
RUN apt-get update && apt-get install -y netcat-openbsd

# Set the working directory in the container
WORKDIR /social_network

# Install dependencies
COPY requirements.txt /social_network/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /social_network/

# Copy the wait script to the container
COPY wait-for-db.sh /social_network/wait-for-db.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["./wait-for-db.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]
