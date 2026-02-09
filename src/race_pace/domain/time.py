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
