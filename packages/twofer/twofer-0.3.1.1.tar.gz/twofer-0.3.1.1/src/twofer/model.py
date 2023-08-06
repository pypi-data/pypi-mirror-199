from typing import Any, NamedTuple


__all__ = ['User', 'Tweet']


class User(NamedTuple):
    id: str
    name: str
    username: str


class Tweet(NamedTuple):
    id: str
    text: str
