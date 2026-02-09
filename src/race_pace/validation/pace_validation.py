class PaceInputValidator:
    @staticmethod
    def validate(minutes: int, seconds: int) -> None:
        if minutes < 0:
            raise ValueError("Pace minutes cannot be negative")

        if not (0 <= seconds <= 59):
            raise ValueError("Pace seconds must be between 0 and 59")

        if minutes == 0 and seconds == 0:
            raise ValueError("Pace must be greater than zero")
