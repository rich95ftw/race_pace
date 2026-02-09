from running_calculator.domain import Time, Distance

class Pace:
    def __init__(self, seconds_per_km: float):
        if seconds_per_km <= 0:
            raise ValueError("Pace must be positive")
        self.seconds_per_km = seconds_per_km

    @classmethod
    def from_time_and_distance(cls, time: Time, distance: Distance):
        return cls(time.seconds / distance.to_km())

    def time_for_distance(self, distance: Distance) -> Time:
        seconds = self.seconds_per_km * distance.to_km()
        return Time(int(round(seconds)))
