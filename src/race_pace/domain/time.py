class Time:
    def __init__(self, seconds: int):
        if seconds < 0:
            raise ValueError("Time cannot be negative")
        self._seconds = seconds

    @classmethod
    def from_hms(cls, hours: int, minutes: int, seconds: int):
        return cls(hours * 3600 + minutes * 60 + seconds)

    @property
    def seconds(self) -> int:
        return self._seconds

    def __add__(self, other: "Time") -> "Time":
        return Time(self.seconds + other.seconds)

    def __str__(self) -> str:
        """
        Returns a formatted string for the UI.
        Examples: '3:05:12' or '45:02'
        """
        hours = self._seconds // 3600
        minutes = (self._seconds % 3600) // 60
        seconds = self._seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def __repr__(self) -> str:
        """Technical representation for debugging."""
        return f"Time(seconds={self._seconds})"