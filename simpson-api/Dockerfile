FROM python:3.7-slim

# Install production dependencies.
COPY requirements.txt /app/requirements.txt
RUN python3 -m pip install --no-cache-dir -U pip && \
    python3 -m pip install --no-cache-dir -r /app/requirements.txt

RUN apt-get update
RUN apt-get install 'ffmpeg' 'libsm6' 'libxext6'  -y

# Copy local code to the container image.
WORKDIR /app
COPY . .


# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
