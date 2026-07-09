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
