from enum import Enum

class DistanceUnit(Enum):
    KM = "km"
    MILES = "miles"

class Distance:
    def __init__(self, value: float, unit: DistanceUnit):
        if value <= 0:
            raise ValueError("Distance must be positive")
        self.value = value
        self.unit = unit

    def to_km(self) -> float:
        if self.unit == DistanceUnit.KM:
            return self.value
        return self.value * 1.609344
