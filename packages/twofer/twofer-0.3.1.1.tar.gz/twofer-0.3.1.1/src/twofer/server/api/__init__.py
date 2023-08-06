from abc import ABC, abstractmethod
from typing import Any, NamedTuple

from twofer.model import *


__all__ = ['APIException', 'AccessTokenResponse',
           'IAuthentication', 'IClient',
           'Authentication', 'Client']


class APIException(Exception):
    pass


class AccessTokenResponse(NamedTuple):
    access_token: str
    token_type: str
    expires_in: int | None = None
    refresh_token: str | None = None
    scope: list[str] | None = None

    @staticmethod
    def from_token_dict(token_dict: dict[str, Any], /) -> 'AccessTokenResponse':

        return AccessTokenResponse(
            token_dict['access_token'],
            token_dict['token_type'],
            token_dict.get('expires_in'),
            token_dict.get('refresh_token'),
            token_dict.get('scope')
        )


class IAuthentication(ABC):

    """OAuth 2.0 authorization protocol for the Twitter API """

    @abstractmethod
    def __init__(self, client_id: str, redirect_uri: str, client_secret: str, /) -> None:
        pass

    @abstractmethod
    def get_authorize_url(self) -> str:
        """Create an authorize URL to allow a user to authenticate via an authentication flow. """
        pass

    @abstractmethod
    def fetch_token(self, url: str, /) -> AccessTokenResponse:
        """Fetch access token with authorization response URL. """
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str, /) -> AccessTokenResponse:
        """Obtain a new access token with a refresh_token.

        OAuth 2.0 Authorization Code Flow with PKCE | Docs | Twitter Developer Platform
        https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        """
        pass

    @abstractmethod
    def invalidate_token(self, access_token: str, /) -> None:
        pass



class IClient(ABC):

    """Authorized client for the Twitter API """

    @abstractmethod
    def __init__(self, access_token: str, /) -> None:
        pass

    @abstractmethod
    def get_me(self) -> User:
        """Returns information about an authorized user. """
        pass

    @abstractmethod
    def post_tweet(self, text: str, /) -> Tweet:
        """Creates a Tweet on behalf of an authenticated user. """
        pass

    @abstractmethod
    def delete_tweet(self, tweet_id: str, /) -> bool:
        """Allow a user or authenticated user ID to delete a Tweet. """
        pass

    @abstractmethod
    def get_user_by_username(self, username: str, /) -> User:
        """Return an information about a user specified by their username. """
        pass

    @abstractmethod
    def get_users_following(self, user_id: str, /) -> list[User]:
        """Return a list of users the specified user ID is following. """
        pass


def Authentication(client_id: str, redirect_uri: str, client_secret: str, /) -> IAuthentication:

    """Return a new instance of the `IAuthentication` implementation. """

    from twofer.server.api.tweepyimpl import AuthenticationImpl
    return AuthenticationImpl(client_id, redirect_uri, client_secret)


def Client(access_token: str, /) -> IClient:

    """Return a new instance of the `IClient` implementation. """

    from twofer.server.api.tweepyimpl import ClientImpl
    return ClientImpl(access_token)
