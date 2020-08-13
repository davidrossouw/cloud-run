"""Authentication functionality for model_api in knative."""
import json
from typing import Optional

import requests
from requests.exceptions import HTTPError
from requests.exceptions import InvalidHeader
from requests.exceptions import ConnectionError

# GCP authentication service
URL_BASE = 'https://oauth2.googleapis.com/tokeninfo?id_token='
# If account returned from above above belongs to one of these domains,
# consider it authenticated.
AUTH_DOMAINS = ['dialpad.com', 'talkiq-data.iam.gserviceaccount.com']


def gcloud_auth(authorization: Optional[str]) -> None:
    """
    Sanity check header and attempt to authenticate.

    Args
        - authorization : GCP auth token as Bearer token in header
                  argument and attemps to authenticate it against
                  GCP's auth service.

    Raises
    ------
        - requests.exceptions.InvalidHeader if token not validated against URL_BASE
                                        or if header malformed
        - requests.exceptions.ConnectionError if authorization unsuccessful.
        - requests.exceptions.HTTPError if failure to parse response
                                       from URL_BASE
    """
    if not authorization:
        raise InvalidHeader('Authorization not found.')

    try:
        bearer, token = authorization.split(' ')
        assert bearer == 'Bearer'
    except (IndexError, AssertionError):
        raise InvalidHeader()

    response = requests.get(URL_BASE + token)
    if response.status_code >= 400:
        raise InvalidHeader('Invalid token.')

    res = response.text
    try:
        email_domain = json.loads(res)['email'].split('@')[1]
    except Exception:
        raise HTTPError('Failed to parse Google OAuth Service response.')

    if email_domain not in AUTH_DOMAINS:
        raise ConnectionError('Invalid permissions.')
