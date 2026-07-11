from datetime import datetime

from core.result import Result


class DateValidator:

    @staticmethod
    def validate_date(date_input: str) -> Result:
        date_format: str = "%Y-%m-%d"
        try:
            validated_date = datetime.strptime(date_input, date_format)
            return Result.valid(value=validated_date)
        except ValueError:
            return Result.invalid(f"Invalid date : {date_input}. Expected 'YYYY-MM-DD'")

    @staticmethod
    def validate_date_time(date_input: str) -> Result:
        date_time_format: str = "%Y-%m-%d %H:%M"
        try:
            validate_date = datetime.strptime(date_input, date_time_format)
            return Result.valid(value=validate_date)
        except ValueError:
            return Result.invalid(
                f"Invalid date time : {date_input}. Expected 'YYYY-MM-DD HH:MM'"
            )
