# twofer.server.flaskapp

from calendar import timegm
from datetime import timedelta
from secrets import token_urlsafe
from time import gmtime, sleep
from typing import Any, Final

from flask import Flask, request, session, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from twofer.helper.functools import time_limited_cache
from twofer.model import *
from twofer.server.api import *
from twofer.server.config import *
from twofer.server.database import *


# database
database: Final[IDatabase] = Database()
database.load()

# Flask
app = Flask(__name__, template_folder=SERVER_TEMPLATE_DIR)
app.permanent_session_lifetime = timedelta(minutes=20)
app.secret_key = FLASK_SECRET_KEY
# Tell Flask it is Behind a Proxy — Flask Documentation (2.1.x)
# https://flask.palletsprojects.com/en/2.1.x/deploying/proxy_fix/
if SERVER_GATEWAY_URL:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

_critical = app.logger.critical
_error = app.logger.error
_warning = app.logger.warning
_info = app.logger.info
_debug = app.logger.debug


authentication = Authentication(
    TWITTER_CLIENT_ID,
    f'{SERVER_GATEWAY_URL}/callback',
    TWITTER_CLIENT_SECRET
)


@time_limited_cache(7200)
def get_owner() -> User:

    client = Client(TWITTER_BEARER_TOKEN)
    return client.get_user_by_username(SERVER_OWNER)


@time_limited_cache(7200)
def owner_following_usernames() -> list[str]:

    client = Client(TWITTER_BEARER_TOKEN)
    owner = client.get_user_by_username(SERVER_OWNER)
    users = client.get_users_following(owner.id)
    return [user.username for user in users]


@time_limited_cache(300)
def user_from_token(user_token: str) -> User:

    client = ensure_unexpired_client(user_token)
    return client.get_me()


def validate_user(user: User, /) -> bool:

    username = user.username
    valid = (
        (username == SERVER_OWNER)
        or (username in SERVER_MEMBERS)
        or (username in owner_following_usernames())
    )
    if not valid:
        _info(f'invalid user: {user}')
    return valid


def user_info_from_access_token_response(atr: AccessTokenResponse, /) -> UserInfo:

    sec = timegm(gmtime())
    return UserInfo(atr.access_token, sec + (atr.expires_in or 0), atr.refresh_token or '')


def ensure_unexpired_client(user_token: str, /) -> IClient:

    user_info = database[user_token]
    access_token = user_info.access_token
    expires_at = user_info.expires_at
    refresh_token = user_info.refresh_token

    client = Client(access_token)

    sec = timegm(gmtime())
    if expires_at <= sec:
        del client
        sleep(1.0)
        access_token_response = authentication.refresh_token(refresh_token)
        sleep(1.0)
        user_info = user_info_from_access_token_response(access_token_response)
        client = Client(user_info.access_token)
        # check if the user is followed by the owner
        me = client.get_me()
        try:
            if validate_user(me):
                database[user_token] = user_info
            else:
                del database[user_token]
                raise Exception(f'invalid user {me}')
        finally:
            database.save()

    return client


@app.route('/')
def index() -> Any:

    user_token = session.get('user_token')
    user = user_from_token(user_token) if user_token is not None else None

    owner = get_owner()

    return render_template('index.html', owner=owner, user=user, user_token=user_token)


@app.route('/login')
def login() -> Any:

    user_token = request.args.get('user_token')
    if user_token and (user_token in database):
        session['user_token'] = user_token
        session.permanent = True

    return app.redirect('/')


@app.route('/logout')
def logout() -> Any:

    session.clear()

    return app.redirect('/')


@app.route('/authenticate')
def authenticate() -> Any:

    auth_url = authentication.get_authorize_url()
    return app.redirect(auth_url)


@app.route('/callback')
def callback() -> Any:

    user_token = session.get('user_token')
    if user_token is not None and user_token in database:
        del database[user_token]
        database.save()
        session.clear()

    try:
        atr = authentication.fetch_token(request.url)
    except Exception as e:
        _info(f'callback() oauth2_user_handler.fetch_token failed: {e}')
        return ['Bad Request'], 400

    user_data = user_info_from_access_token_response(atr)
    access_token: str = user_data.access_token

    client = Client(access_token)
    user_me = client.get_me()
    if not validate_user(user_me):
        return ['Forbidden'], 403

    user_token = token_urlsafe()
    _debug(f'granted user_token {user_token} for {user_me}')
    database[user_token] = user_data
    database.save()

    session['user_token'] = user_token
    session.permanent = True

    return render_template('callback.html', user_token=user_token)


@app.route('/leave/<user_token>')
def leave(user_token: str) -> Any:

    if user_token in database:
        user_data = database[user_token]
        access_token = user_data.access_token
        authentication.invalidate_token(access_token)
        try:
            del database[user_token]
        except KeyError:
            pass
        database.save()
        session.clear()
    return app.redirect('/')


@app.route('/2/tweets/<tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id: str) -> Any:

    try:
        user_token = request.args['user_token']
    except KeyError as e:
        _debug(f'delete_tweet(): {e}')
        return ['Bad request'], 400

    client = ensure_unexpired_client(user_token)
    if client is None:
        return ['Bad request'], 400

    deleted = client.delete_tweet(tweet_id)
    return {'data': {'deleted': deleted}}


@app.route('/2/tweets', methods=['POST'])
def create_tweet() -> Any:

    try:
        user_token = request.args['user_token']
        data = request.get_json()
        if not isinstance(data, dict):
            return ['Bad request'], 400
        text = data.get('text')
        if not text:
            return ['Bad request'], 400
    except Exception as e:
        _debug(f'create_tweet(): {e}')
        return ['Bad request'], 400

    client = ensure_unexpired_client(user_token)
    if client is None:
        _debug('client is None')
        return ['Bad request'], 400

    tweet = client.post_tweet(text)
    return {'data': tweet._asdict()}


def main() -> None:
    app.run(SERVER_HOST, SERVER_PORT)


if __name__ == '__main__':
    main()
