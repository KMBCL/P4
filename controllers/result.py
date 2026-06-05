from __future__ import annotations

from typing import Any


class Result:

    def __init__(
        self, is_valid: bool, reason: str | None = None, value: Any | None = None
    ) -> None:
        self.is_valid: bool = is_valid
        self.reason = reason
        self.value = value

    @classmethod
    def valid(cls, value: Any | None = None) -> Result:
        return Result(is_valid=True, value=value)

    @classmethod
    def invalid(cls, reason: str) -> Result:
        return Result(is_valid=False, reason=reason)

    def __bool__(self) -> bool:
        return self.is_valid

    @property
    def required_reason(self) -> str:
        if self.reason is None:
            raise ValueError("Reason is not defined")

        return self.reason

    @property
    def required_value(self) -> Any:
        if self.value is None:
            raise ValueError("Value is not defined")

        return self.value
