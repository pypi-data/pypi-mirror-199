from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemsArchiveReason(Enums.KnownString):
    MADE_IN_ERROR = "Made in error"
    RETIRED = "Retired"
    OTHER = "Other"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemsArchiveReason":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemsArchiveReason must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemsArchiveReason", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemsArchiveReason, getattr(newcls, "_UNKNOWN"))
