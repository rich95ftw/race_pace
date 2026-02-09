class TimeInputValidator:
    @staticmethod
    def validate(hours: int, minutes: int, seconds: int) -> None:
        if hours < 0:
            raise ValueError("Hours cannot be negative")

        if not (0 <= minutes <= 59):
            raise ValueError("Minutes must be between 0 and 59")

        if not (0 <= seconds <= 59):
            raise ValueError("Seconds must be between 0 and 59")

        if hours == 0 and minutes == 0 and seconds == 0:
            raise ValueError("Time must be greater than zero")
