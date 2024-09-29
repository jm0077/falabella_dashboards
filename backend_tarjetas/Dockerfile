# Use a Python base image
FROM python:3.9-slim

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 8080

# Command to run the application
CMD ["python", "backend_bancos.py"]