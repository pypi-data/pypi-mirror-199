"""twofer.server.api.tweepyimpl - Twitter API Tweepy implementation

Tweepy
https://www.tweepy.org
https://docs.tweepy.org/en/stable/
https://github.com/tweepy/tweepy
"""

import os
import logging
from time import sleep
from urllib.parse import urlencode

import tweepy

from twofer.model import *
from twofer.server.api import *


__all__ = ['AuthenticationImpl', 'ClientImpl']


logging.basicConfig()
_logger = logging.getLogger(__name__)
if os.environ.get('DEBUG'):
    _logger.setLevel('DEBUG')


class AuthenticationImpl(IAuthentication):

    def __init__(self, client_id: str, redirect_uri: str, client_secret: str, /) -> None:

        self._client_id = client_id
        self._redirect_uri = redirect_uri
        self._client_secret = client_secret
        # Tweepy
        # OAuth 2.0 Authorization Code Flow with PKCE | Docs | Twitter Developer Platform
        # https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        self._oauth2_user_handler = tweepy.OAuth2UserHandler(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=['tweet.read', 'tweet.write', 'users.read', 'follows.read', 'offline.access'],
            client_secret=client_secret
        )

    def get_authorize_url(self) -> str:

        return self._oauth2_user_handler.get_authorization_url()

    def fetch_token(self, url: str, /) -> AccessTokenResponse:

        token_dict = self._oauth2_user_handler.fetch_token(url)
        return AccessTokenResponse.from_token_dict(token_dict)

    def refresh_token(self, refresh_token: str, /) -> AccessTokenResponse:

        _logger.debug('refresh_token')
        token_dict = self._oauth2_user_handler.refresh_token(
            'https://api.twitter.com/2/oauth2/token',
            refresh_token,
            auth=self._oauth2_user_handler.auth,
            timeout=5)
        _logger.debug(f'{token_dict=}')
        return AccessTokenResponse.from_token_dict(token_dict)

    def invalidate_token(self, access_token: str, /) -> None:

        query_str = urlencode({'access_token': access_token})
        url = f'https://api.twitter.com/2/oauth2/invalidate_token?{query_str}'
        self._oauth2_user_handler.post(url, auth=None)



class ClientImpl(IClient):

    def __init__(self, access_token: str, /) -> None:

        self._access_token = access_token
        self._tweepy_client = tweepy.Client(access_token)

    def get_me(self) -> User:

        response = self._tweepy_client.get_me(user_auth=False)
        if not isinstance(response, tweepy.Response):
            raise APIException()
        data = response.data
        return User(data['id'], data['name'], data['username'])

    def post_tweet(self, text: str) -> Tweet:

        """Creates a Tweet on behalf of an authenticated user. """

        response = self._tweepy_client.create_tweet(text=text, user_auth=False)
        if not isinstance(response, tweepy.Response):
            raise APIException(response)
        data = response.data
        return Tweet(data['id'], data['text'])

    def delete_tweet(self, tweet_id: str) -> bool:

        """Allow a user or authenticated user ID to delete a Tweet. """

        response = self._tweepy_client.delete_tweet(tweet_id, user_auth=False)
        if not isinstance(response, tweepy.Response):
            raise APIException(response)
        return response.data['deleted']

    def get_user_by_username(self, username: str) -> User:

        """Return an information about a user specified by their username. """

        response = self._tweepy_client.get_user(username=username)
        if not isinstance(response, tweepy.Response):
            raise APIException(response)
        data = response.data
        return User(data['id'], data['name'], data['username'])

    def get_users_following(self, user_id: str) -> list[User]:

        """Return a list of users the specified user ID is following. """

        users = []
        next_token = None
        while True:
            response = self._tweepy_client.get_users_following(
                user_id, max_results=1000, pagination_token=next_token)
            if not isinstance(response, tweepy.Response):
                raise APIException(response)
            users.extend([User(data['id'], data['name'], data['username'])
                          for data in response.data])
            next_token = response.meta.get('next_token')
            if not next_token:
                break
        return users
