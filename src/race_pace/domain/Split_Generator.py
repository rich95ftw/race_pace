from race_pace.domain import Pace, Split, Time

class SplitGenerator:
    def __init__(self, pace: Pace):
        self.pace = pace

    def generate_splits(
        self,
        total_distance_km: float,
        interval_km: float = 1.0,
        include_half_marathon: bool = False
    ) -> list[Split]:

        splits = []
        current = 0.0

        while current + interval_km < total_distance_km:
            current += interval_km
            time = Time(int(self.pace.seconds_per_km * current))
            splits.append(Split(current, time))

            if include_half_marathon and current < 21.0975 < current + interval_km:
                hm_time = Time(int(self.pace.seconds_per_km * 21.0975))
                splits.append(Split(21.0975, hm_time))

        # Final split
        final_time = Time(int(self.pace.seconds_per_km * total_distance_km))
        splits.append(Split(total_distance_km, final_time))

        return sorted(splits, key=lambda s: s.distance_km)
