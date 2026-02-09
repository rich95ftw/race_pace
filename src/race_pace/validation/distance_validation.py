class DistanceInputValidator:
    @staticmethod
    def validate(distance_type: str, custom_value: float) -> None:
        if distance_type == "custom":
            if custom_value <= 0:
                raise ValueError("Custom distance must be greater than zero")
