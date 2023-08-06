# twofer.server.database.jsonimpl - JSON database implementation

import json
from typing import Any

from twofer.server.database import *


class DatabaseImpl(IDatabase):

    def __init__(self, filename: str, /) -> None:
        self._filename = filename
        self._d: dict[str, dict[str, Any]] = {}

    def __len__(self) -> int:
        return self._d.__len__()

    def __getitem__(self, user_token: str) -> UserInfo:
        return UserInfo(**self._d.__getitem__(user_token))

    def __setitem__(self, user_token: str, user_info: UserInfo) -> None:
        self._d.__setitem__(user_token, user_info._asdict())

    def __delitem__(self, user_token: str) -> None:
        self._d.__delitem__(user_token)

    def __contains__(self, user_token: str) -> bool:
        return self._d.__contains__(user_token)

    def load(self) -> None:
        try:
            with open(self._filename, encoding='utf-8') as f:
                self._d.clear()
                self._d.update(json.load(f))
        except FileNotFoundError:
            pass

    def save(self) -> None:
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(self._d, f, indent=2)
