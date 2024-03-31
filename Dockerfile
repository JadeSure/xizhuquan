# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .
COPY /data .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create volumes for data and output
VOLUME /app/data
VOLUME /app/output

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV NAME World

# Run load_data.py when the container launches
CMD ["python3", "process_data.py"]
