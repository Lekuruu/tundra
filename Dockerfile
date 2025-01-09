FROM python:3.13-slim

# Copy the source code to /app
WORKDIR /app
COPY . /app

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
ARG WEB_PORT
EXPOSE $WEB_PORT

# Run app.py when the container launches
CMD ["python", "main.py"]