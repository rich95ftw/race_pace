from running_calculator.domain import Time, Distance, Pace

class CalculatorService:
    def pace_to_time(self, pace: Pace, distance: Distance) -> Time:
        return pace.time_for_distance(distance)

    def time_to_pace(self, time: Time, distance: Distance) -> Pace:
        return Pace.from_time_and_distance(time, distance)
