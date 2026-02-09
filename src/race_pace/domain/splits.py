from running_calculator.domain import Time

class Split:
    def __init__(self, distance_km: float, cumulative_time: Time):
        self.distance_km = distance_km
        self.cumulative_time = cumulative_time
