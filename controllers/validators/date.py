"""Validates the dates and timestamps typed by the user."""

from datetime import datetime

from core.result import Result


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
        date_format: str = "%Y-%m-%d"
        try:
            validated_date = datetime.strptime(date_input, date_format)
            return Result.valid(value=validated_date)
        except ValueError:
            return Result.invalid(f"Invalid date : {date_input}. Expected 'YYYY-MM-DD'")

    @staticmethod
    def validate_date_time(date_input: str) -> Result:
        """Validates a timestamp against the 'YYYY-MM-DD HH:MM' format.

        Used for the start and end timestamps of a round, which need the time of
        day that a plain date does not carry.

        Args:
            date_input (str): The raw timestamp typed by the user.

        Returns:
            Result:
                - A valid result carrying the parsed ``datetime``.
                - An invalid one whose reason repeats the offending input.
        """
        date_time_format: str = "%Y-%m-%d %H:%M"
        try:
            validate_date = datetime.strptime(date_input, date_time_format)
            return Result.valid(value=validate_date)
        except ValueError:
            return Result.invalid(
                f"Invalid date time : {date_input}. Expected 'YYYY-MM-DD HH:MM'"
            )
