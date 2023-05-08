# syntax=docker/dockerfile:1

FROM python:3.8.5-slim-buster

# Set the working directory to /PyFlora/flaskr
WORKDIR /PyFlora/flaskr

# Copy the requirements file into the container at /PyFlora
COPY requirements.txt /PyFlora

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /PyFlora/requirements.txt

# Copy the current directory contents into the container at /PyFlora/flaskr
COPY . /PyFlora/flaskr

# Set the environment variable for Flask
ENV FLASK_APP=flaskr

# Expose port 5000 for Flask app
EXPOSE 5000

# Run the command to start Flask server
CMD ["flask", "run", "--host=0.0.0.0"]