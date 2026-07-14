"""Provides the outcome every validation and every service reports."""

from __future__ import annotations

from typing import Any


class Result:
    """Reports an outcome as valid or invalid, and carries what it produced.

    A result is truthy when it holds a value, not when it is valid.
    """

    def __init__(
        self,
        is_valid: bool,
        reason: str | None = None,
        success_message: str | None = None,
        value: Any | None = None,
    ) -> None:
        """Holds the outcome, and what it produced.

        Args:
            is_valid (bool): Whether the outcome is a success.
            reason (str | None): Why the outcome failed.
            success_message (str | None): What to tell the user on success.
            value (Any | None): What the outcome produced.
        """
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
        """Reports a successful outcome.

        Args:
            value (Any | None): What the outcome produced.
            success_message (str | None): What to tell the user.

        Returns:
            Result: The valid result.
        """
        return cls(is_valid=True, value=value, success_message=success_message)

    @classmethod
    def invalid(cls, reason: str) -> Result:
        """Reports a failed outcome.

        Args:
            reason (str): Why the outcome failed.

        Returns:
            Result: The invalid result.
        """
        return cls(is_valid=False, reason=reason)

    def __bool__(self) -> bool:
        """Tells whether the result holds a value.

        Returns:
            bool: True when the result holds a value.

        Raises:
            ValueError: When the result is valid and holds no value, or is
                invalid and holds one.
        """
        if self._is_valid and self._value is None:
            raise ValueError(
                "Ambiguous state. Expected a value,  if _is_valid is True."
            )

        if not self._is_valid and self._value is not None:
            raise ValueError(
                "Ambiguous state. Not expected a value,  if _is_valid is False."
            )

        return self._value is not None

    def get_reason(self) -> str:
        """Reads why the outcome failed.

        Returns:
            str: The reason.

        Raises:
            ValueError: When the result holds no reason.
        """
        if self._reason is None:
            raise ValueError("Reason is not defined")

        return self._reason

    def get_value(self) -> Any:
        """Reads what the outcome produced.

        Returns:
            Any: The value.

        Raises:
            ValueError: When the result holds no value.
        """
        if self._value is None:
            raise ValueError("Value is not defined")

        return self._value

    def get_success_message(self) -> str:
        """Reads what to tell the user on success.

        Returns:
            str: The message.

        Raises:
            ValueError: When the result holds no message.
        """
        if self._success_message is None:
            raise ValueError("success_message is not defined")

        return self._success_message

    def is_valid(self) -> bool:
        """Tells whether the outcome is a success.

        Returns:
            bool: True when the outcome succeeded.
        """
        return self._is_valid

    def __repr__(self) -> str:
        """Represents the result by its value, its validity and its reason.

        Returns:
            str: The representation of the result.
        """
        return f"value : {self._value} - valid : {self._is_valid} - reason : {self._reason}"
