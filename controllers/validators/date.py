from datetime import datetime

from controllers.result import Result


class DateValidator:

    def validate_date(self, date_input: str) -> Result:
        date_format: str = "%Y-%m-%d"
        try:
            datetime.strptime(date_input, date_format)
            return Result.valid()
        except ValueError:
            return Result.invalid(f"Invalid date : {date_input}. Expected 'YYYY-MM-DD'")
