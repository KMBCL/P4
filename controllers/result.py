from __future__ import annotations


class Result:

    def __init__(self, is_valid: bool, reason: str | None = None) -> None:
        self.is_valid: bool = is_valid
        self.reason = reason

    @classmethod
    def valid(cls) -> Result:
        return Result(is_valid=True)

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
