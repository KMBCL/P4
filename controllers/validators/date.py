"""Validates the dates typed by the user."""

from datetime import datetime

from core.result import Result
from core.core_formats import DATE, DATE_HINT


class DateValidator:
    """Parses user dates, and reports a malformed one as an invalid result."""

    @staticmethod
    def validate_date(date_input: str) -> Result:
        """Validates a calendar date against the 'YYYY-MM-DD' format.

        Args:
            date_input (str): The raw date typed by the user.

        Returns:
            Result:
                - A valid result carrying the parsed ``datetime``.
                - An invalid one whose reason repeats the offending input.
        """
        try:
            validated_date = datetime.strptime(date_input, DATE)
            return Result.valid(value=validated_date)
        except ValueError:
            return Result.invalid(
                f"Invalid date : {date_input}. Expected '{DATE_HINT}'"
            )
