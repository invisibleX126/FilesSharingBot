# Use the python:3.8-slim-buster image as the base image
FROM python:3.8-slim-buster
# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt requirements.txt
# Install the dependencies listed in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the current directory to the working directory
COPY . .

# Run the main.py file when the container is started
CMD python3 main.py
