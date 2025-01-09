FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install required packages
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to /app
COPY . /app

# Expose the port the app runs on
ARG WEB_PORT
EXPOSE $WEB_PORT

# Run app.py when the container launches
CMD ["python", "main.py"]