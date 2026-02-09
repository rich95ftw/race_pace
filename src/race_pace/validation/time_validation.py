class TimeValidator:
    @staticmethod
    def validate_hms(hours, minutes, seconds):
        if not all(isinstance(x, int) for x in (hours, minutes, seconds)):
            raise ValueError("Time values must be integers")
        if minutes not in range(60) or seconds not in range(60):
            raise ValueError("Minutes and seconds must be 0–59")
