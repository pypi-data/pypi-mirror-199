# twofer.server.database - Database model and interface definitions

from abc import ABC, abstractmethod
from typing import Any, NamedTuple


__all__ = ['UserInfo', 'IDatabase', 'Database']


class UserInfo(NamedTuple):
    access_token: str
    expires_at: int
    refresh_token: str


class IDatabase(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of user records in the database. """
        pass

    @abstractmethod
    def __getitem__(self, user_token: str) -> UserInfo:
        """Return the `UserInfo` record associated to the `user_token`. """
        pass

    @abstractmethod
    def __setitem__(self, user_token: str, user_info: UserInfo) -> None:
        """Set `UserInfo` record to `user_token`. """
        pass

    @abstractmethod
    def __delitem__(self, user_token: str) -> None:
        """Remove `db[user_token]` from the database. """
        pass

    @abstractmethod
    def __contains__(self, user_token: str) -> bool:
        """Return whether database contains a record for `user_token`. """
        pass

    @abstractmethod
    def load(self) -> None:
        """Load records from the implementation-specific location. """
        pass

    @abstractmethod
    def save(self) -> None:
        """Store records to the implementation-specific location. """
        pass


def Database() -> IDatabase:

    """Return a new instance of the `IDatabase` implementation. """

    from twofer.server.config import SERVER_DATA_FILE
    from twofer.server.database.jsonimpl import DatabaseImpl
    return DatabaseImpl(SERVER_DATA_FILE)
