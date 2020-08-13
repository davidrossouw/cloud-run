# Code adapted from: https://codelabs.developers.google.com/codelabs/cloud-run-hello-python3/#0

import argparse
import google.cloud.logging
import logging
import os

from auth import gcloud_auth

from flask import Flask, request

client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.get_default_handler()
client.setup_logging()

app = Flask(__name__)


@app.before_request
def authenticate_request():
    """Authenticates every request."""
    gcloud_auth(request.headers.get('Authorization'))


@app.route('/', methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    who = request.args.get('who', 'there')
    # Write a log entry
    logging.info(f'who: {who}')

    return f'Hello {who}!\n'


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
