from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SessionUpdateStatus(Enums.KnownString):
    COMPLETED_WITH_WARNINGS = "COMPLETED_WITH_WARNINGS"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SessionUpdateStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of SessionUpdateStatus must be a string (encountered: {val})")
        newcls = Enum("SessionUpdateStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SessionUpdateStatus, getattr(newcls, "_UNKNOWN"))
