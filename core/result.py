from __future__ import annotations

from typing import Any


class Result:

    def __init__(
        self,
        is_valid: bool,
        reason: str | None = None,
        success_message: str | None = None,
        value: Any | None = None,
    ) -> None:
        self._is_valid: bool = is_valid
        self._reason = reason
        self._success_message = success_message
        self._value = value

    @classmethod
    def valid(
        cls,
        value: Any | None = None,
        success_message: str | None = None,
    ) -> Result:
        return cls(is_valid=True, value=value, success_message=success_message)

    @classmethod
    def invalid(cls, reason: str) -> Result:
        return cls(is_valid=False, reason=reason)

    def __bool__(self) -> bool:
        # revoir pour if doit vérifer un objet vide
        return self._is_valid

    def get_reason(self) -> str:
        if self._reason is None:
            raise ValueError("Reason is not defined")

        return self._reason

    def get_value(self) -> Any:
        if self._value is None:
            raise ValueError("Value is not defined")

        return self._value

    def get_success_message(self) -> str:
        if self._success_message is None:
            raise ValueError("success_message is not defined")

        return self._success_message
