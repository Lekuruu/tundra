FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install required packages
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# This dockerfile requires you to have a volume that contains the source code for tundra
# You can add this line, if you don't want to use a volume:
# COPY . .

VOLUME /app

# Expose the ports used by the API and world server
ARG WEB_PORT=80
ARG METAPLACE_PORT=7003
EXPOSE $WEB_PORT $METAPLACE_PORT

# Select `api` or `world` through the container command
ENTRYPOINT ["python", "main.py"]
CMD ["api"]
