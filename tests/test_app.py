import pytest
import tkinter as tk
from race_pace.gui.app import RunningCalculatorApp
from race_pace.domain.pace import Pace
from race_pace.domain.distance import Distance, DistanceUnit


@pytest.fixture
def app():
    """Create an app instance without running mainloop."""
    application = RunningCalculatorApp()
    yield application
    application.root.destroy()


# --- 1. App Initialization ---

class TestAppInitialization:
    def test_app_creates_without_error(self, app):
        assert app.root is not None

    def test_default_mode_is_time_to_pace(self, app):
        assert app.mode.get() == "time_to_pace"

    def test_default_distance_type_is_marathon(self, app):
        assert app.distance_type.get() == "marathon"

    def test_splits_table_exists(self, app):
        assert app.split_table is not None

    def test_splits_table_has_correct_headings(self, app):
        columns = app.split_table["columns"]
        assert "distance" in columns
        assert "time" in columns


# --- 2. Distance Mapping ---

class TestDistanceMapping:
    def test_marathon_distance(self, app):
        app.distance_type.set("marathon")
        dist = app._get_distance_object()
        assert dist.to_km() == pytest.approx(42.195)

    def test_half_marathon_distance(self, app):
        app.distance_type.set("half")
        dist = app._get_distance_object()
        assert dist.to_km() == pytest.approx(21.0975)

    def test_10k_distance(self, app):
        app.distance_type.set("10k")
        dist = app._get_distance_object()
        assert dist.to_km() == pytest.approx(10.0)

    def test_custom_distance_km(self, app):
        app.distance_type.set("custom")
        app.custom_distance.set(15.0)
        app.distance_unit.set("km")
        dist = app._get_distance_object()
        assert dist.to_km() == pytest.approx(15.0)

    def test_custom_distance_miles(self, app):
        app.distance_type.set("custom")
        app.custom_distance.set(10.0)
        app.distance_unit.set("miles")
        dist = app._get_distance_object()
        assert dist.to_km() == pytest.approx(16.09344)


# --- 3. Input Mode Switching ---

class TestInputModeSwitching:
    def _child_labels(self, app):
        """Return text of all Label widgets in the input container."""
        return [
            w.cget("text")
            for w in app.input_container.winfo_children()
            if isinstance(w, (tk.Label, __import__("tkinter").ttk.Label))
        ]

    def test_time_to_pace_shows_time_fields(self, app):
        app.mode.set("time_to_pace")
        app._refresh_input_mode()
        labels = self._child_labels(app)
        assert "Hours:" in labels
        assert "Mins:" in labels
        assert "Secs:" in labels

    def test_pace_to_time_shows_pace_fields(self, app):
        app.mode.set("pace_to_time")
        app._refresh_input_mode()
        labels = self._child_labels(app)
        assert "Pace (min/km):" in labels


# --- 4. Custom Distance Toggle ---

class TestCustomDistanceToggle:
    def test_custom_shows_entry_and_unit(self, app):
        app.distance_type.set("custom")
        app.root.update_idletasks()
        assert app.custom_distance_entry.winfo_manager() != ""
        assert app.distance_unit_combo.winfo_manager() != ""

    def test_marathon_hides_custom_fields(self, app):
        app.distance_type.set("custom")
        app.root.update_idletasks()
        app.distance_type.set("marathon")
        app.root.update_idletasks()
        assert app.custom_distance_entry.winfo_manager() == ""
        assert app.distance_unit_combo.winfo_manager() == ""


# --- 5. Validation ---

class TestValidation:
    def test_valid_time_inputs_pass(self, app):
        app.mode.set("time_to_pace")
        app.hours.set(3)
        app.minutes.set(30)
        app.seconds.set(0)
        assert app._validate_all() is True

    def test_zero_time_fails(self, app):
        app.mode.set("time_to_pace")
        app.hours.set(0)
        app.minutes.set(0)
        app.seconds.set(0)
        assert app._validate_all() is False

    def test_valid_pace_inputs_pass(self, app):
        app.mode.set("pace_to_time")
        app.pace_minutes.set(5)
        app.pace_seconds.set(30)
        assert app._validate_all() is True

    def test_zero_pace_fails(self, app):
        app.mode.set("pace_to_time")
        app.pace_minutes.set(0)
        app.pace_seconds.set(0)
        assert app._validate_all() is False

    def test_custom_distance_zero_fails(self, app):
        app.distance_type.set("custom")
        app.custom_distance.set(0)
        app.mode.set("time_to_pace")
        app.hours.set(1)
        app.minutes.set(0)
        app.seconds.set(0)
        assert app._validate_all() is False


# --- 6. Splits Calculation ---

class TestSplitsCalculation:
    def _row_count(self, app):
        return len(app.split_table.get_children())

    def _get_rows(self, app):
        return [
            app.split_table.item(child, "values")
            for child in app.split_table.get_children()
        ]

    def test_10k_produces_10_rows(self, app):
        pace = Pace(300)  # 5:00/km
        distance = Distance(10.0, DistanceUnit.KM)
        app._update_splits_table(pace, distance)
        assert self._row_count(app) == 10

    def test_marathon_produces_43_rows(self, app):
        pace = Pace(300)  # 5:00/km
        distance = Distance(42.195, DistanceUnit.KM)
        app._update_splits_table(pace, distance)
        # 42 whole km + 1 fractional (0.195 km)
        assert self._row_count(app) == 43

    def test_first_split_correct_time(self, app):
        pace = Pace(300)  # 5:00/km
        distance = Distance(10.0, DistanceUnit.KM)
        app._update_splits_table(pace, distance)
        rows = self._get_rows(app)
        assert rows[0][0] == "1 km"
        assert rows[0][1] == "05:00"

    def test_last_split_shows_total_distance(self, app):
        pace = Pace(300)
        distance = Distance(42.195, DistanceUnit.KM)
        app._update_splits_table(pace, distance)
        rows = self._get_rows(app)
        assert rows[-1][0] == "42.195 km"

    def test_recalculating_clears_previous_rows(self, app):
        pace = Pace(300)
        dist_10k = Distance(10.0, DistanceUnit.KM)
        dist_5k = Distance(5.0, DistanceUnit.KM)
        app._update_splits_table(pace, dist_10k)
        assert self._row_count(app) == 10
        app._update_splits_table(pace, dist_5k)
        assert self._row_count(app) == 5


# --- 7. End-to-End Calculation ---

class TestEndToEndCalculation:
    def _row_count(self, app):
        return len(app.split_table.get_children())

    def test_time_to_pace_populates_splits(self, app):
        app.mode.set("time_to_pace")
        app.distance_type.set("10k")
        app.hours.set(0)
        app.minutes.set(50)
        app.seconds.set(0)
        app._handle_calculation()
        assert self._row_count(app) > 0

    def test_pace_to_time_populates_splits(self, app):
        app.mode.set("pace_to_time")
        app._refresh_input_mode()
        app.distance_type.set("10k")
        app.pace_minutes.set(5)
        app.pace_seconds.set(0)
        app._handle_calculation()
        assert self._row_count(app) == 10
