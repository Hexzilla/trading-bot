import datetime
import logging
import os
from urllib.parse import urlparse

from authlib.integrations.httpx_client import OAuth2Client
from flask import Flask, redirect, request, abort

from brokers.tda.auth.custom_auth import fetch_and_register_token_from_redirect, get_token_path, normalize_api_key
from brokers.tda.db import db_auth

API_ENDPOINT = 'https://api.tdameritrade.com'
AUTH_ENDPOINT = 'https://auth.tdameritrade.com/auth'
REFERER_URL = 'https://auth.tdameritrade.com/'
REDIRECT_URL = 'https://localhost:8443/fetch_authorization_code'
AUTHORIZE_URL = 'https://localhost/authorize?api_key=TDA_API_KEY'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(52)

logins = None
with app.app_context():
    db_auth.delete_all()
    logins = {}


def get_oauth(api_key):
    api_key = normalize_api_key(api_key)
    return OAuth2Client(api_key, redirect_uri=REDIRECT_URL)


def get_logger():
    return logging.getLogger(__name__)


def get_authorization_url(oauth):
    get_logger().info('Creating new token with redirect URL \'%s\' ', REDIRECT_URL)
    authorization_url, state = oauth.create_authorization_url(AUTH_ENDPOINT)
    return authorization_url


@app.route('/authorize')
def authorize():
    args = request.args
    if 'api_key' not in args:
        return 'Usage: ' + AUTHORIZE_URL

    api_key = normalize_api_key(args.get('api_key'))
    global logins
    oauth = get_oauth(api_key)

    with app.app_context():
        logins[api_key] = get_oauth(api_key)
        authorization_url = get_authorization_url(oauth)

    # Get the state
    results = urlparse(authorization_url)
    state = results.query.split('&')[3].split('=')[1]
    now = datetime.datetime.utcnow()
    db_auth.delete_by_api_key(api_key)
    inserted_row_id = db_auth.insert_auth(
        (api_key, state, now + datetime.timedelta(minutes=2)))

    return redirect(authorization_url, code=302)


@app.route('/fetch_authorization_code')
def fetch_authorization_code():
    # Validate the referrer: The redirected URL must be from 'https://auth.tdameritrade.com/'
    referrer = request.referrer
    if referrer is None or referrer != REFERER_URL:
        abort(401)

    # Get the authorization code and Oauth state from the redirected URL
    state = request.args.get('state')

    # Get the row that has the Oauth state
    row = db_auth.select_by_oauth_state(state)
    if len(row) != 1:
        abort(401)

    auth_row = row[0]
    api_key = auth_row[0]
    expiration_date = datetime.datetime.strptime(auth_row[2], '%Y-%m-%d %H:%M:%S.%f')

    # Validate the redirection timeout - valid for 2 minutes
    now = datetime.datetime.utcnow()
    if now > expiration_date:
        abort(401)

    global logins
    with app.app_context():
        oauth = logins.get(api_key)

    # Save the access token into file
    redirected_url = request.host_url.rstrip('/') + request.full_path
    fetch_and_register_token_from_redirect(oauth, redirected_url, api_key,
                                           get_token_path(api_key), None, False, True)

    # Clean up
    logins.pop(api_key)
    db_auth.delete_by_api_key(api_key)

    return 'Successfully authorized the auto trader to access your TDAmeritrade account.'
