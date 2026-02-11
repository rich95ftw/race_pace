import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

# Domain and Service Imports
from race_pace.services.calculator import CalculatorService
from race_pace.domain.pace import Pace
from race_pace.domain.time import Time
from race_pace.domain.distance import Distance, DistanceUnit
from race_pace.validation.time_validation import TimeInputValidator
from race_pace.validation.distance_validation import DistanceInputValidator
from race_pace.validation.pace_validation import PaceInputValidator

class RunningCalculatorApp:
    """
    Main Application class for the Race Pace Calculator.
    Handles the UI orchestration and ties the domain logic to the view.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Running Calculator")
        
        # Service Layer
        self.calculator = CalculatorService()

        # State Variables
        self._init_variables()
        
        # Build UI
        self._setup_ui()

    def _init_variables(self) -> None:
        """Initialize all Tkinter variables used for data binding."""
        self.mode = tk.StringVar(value="time_to_pace")
        self.distance_type = tk.StringVar(value="marathon")
        self.custom_distance = tk.DoubleVar(value=10.0)
        self.distance_unit = tk.StringVar(value="km")
        
        # Time inputs
        self.hours = tk.IntVar(value=3)
        self.minutes = tk.IntVar(value=0)
        self.seconds = tk.IntVar(value=0)
        
        # Pace inputs
        self.pace_minutes = tk.IntVar(value=5)
        self.pace_seconds = tk.IntVar(value=0)
        
        # UI Reference holder
        self.input_container: Optional[ttk.LabelFrame] = None

    def _setup_ui(self) -> None:
        """Create the primary layout structure."""
        self._create_mode_selector().grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self._create_distance_selector().grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Placeholder for dynamic input frame
        self.input_container = ttk.LabelFrame(self.root, text="Input Details")
        self.input_container.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self._refresh_input_mode()

        self._create_action_buttons().grid(row=3, column=0, pady=10)
        self._create_splits_display().grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

    # --- UI Component Factories ---

    def _create_mode_selector(self) -> ttk.LabelFrame:
        """Creates the radio buttons to toggle between time and pace calculations."""
        frame = ttk.LabelFrame(self.root, text="Calculation Mode")
        
        modes = [
            ("Finish Time → Pace", "time_to_pace"),
            ("Pace → Finish Time", "pace_to_time")
        ]
        
        for i, (text, mode) in enumerate(modes):
            ttk.Radiobutton(
                frame, text=text, variable=self.mode, 
                value=mode, command=self._refresh_input_mode
            ).grid(row=0, column=i, padx=5, sticky="w")
            
        return frame

    def _create_distance_selector(self) -> ttk.LabelFrame:
        """Creates the dropdown and entry for race distance."""
        frame = ttk.LabelFrame(self.root, text="Distance")
        
        ttk.Combobox(
            frame, textvariable=self.distance_type,
            values=["marathon", "half", "10k", "custom"],
            state="readonly", width=12
        ).grid(row=0, column=0, padx=5)

        ttk.Entry(frame, textvariable=self.custom_distance, width=8).grid(row=0, column=1)
        
        ttk.Combobox(
            frame, textvariable=self.distance_unit,
            values=["km", "miles"], state="readonly", width=8
        ).grid(row=0, column=2, padx=5)
        
        return frame

    def _refresh_input_mode(self) -> None:
        """Swaps the input fields based on the selected calculation mode."""
        if not self.input_container:
            return

        # Clear existing widgets in the container
        for widget in self.input_container.winfo_children():
            widget.destroy()

        if self.mode.get() == "time_to_pace":
            self._build_time_inputs(self.input_container)
        else:
            self._build_pace_inputs(self.input_container)

    def _build_time_inputs(self, parent: ttk.Widget) -> None:
        """Finish Time specific input fields."""
        ttk.Label(parent, text="Hours:").grid(row=0, column=0)
        ttk.Spinbox(parent, from_=0, to=23, textvariable=self.hours, width=5).grid(row=0, column=1)
        
        ttk.Label(parent, text="Mins:").grid(row=0, column=2)
        ttk.Spinbox(parent, from_=0, to=59, textvariable=self.minutes, width=5).grid(row=0, column=3)
        
        ttk.Label(parent, text="Secs:").grid(row=0, column=4)
        ttk.Spinbox(parent, from_=0, to=59, textvariable=self.seconds, width=5).grid(row=0, column=5)

    def _build_pace_inputs(self, parent: ttk.Widget) -> None:
        """Pace specific input fields."""
        ttk.Label(parent, text="Pace (min/km):").grid(row=0, column=0)
        ttk.Spinbox(parent, from_=0, to=20, textvariable=self.pace_minutes, width=5).grid(row=0, column=1)
        ttk.Spinbox(parent, from_=0, to=59, textvariable=self.pace_seconds, width=5).grid(row=0, column=2)

    def _create_action_buttons(self) -> ttk.Frame:
        frame = ttk.Frame(self.root)
        ttk.Button(frame, text="Calculate", command=self._handle_calculation).pack()
        return frame

    def _create_splits_display(self) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(self.root, text="Splits")
        
        self.split_table = ttk.Treeview(
            frame, columns=("distance", "time"), show="headings", height=8
        )
        self.split_table.heading("distance", text="Distance (km)")
        self.split_table.heading("time", text="Cumulative Time")
        self.split_table.pack(fill="both", expand=True, padx=5, pady=5)
        
        return frame

    # --- Logic & Handlers ---

    def _get_distance_object(self) -> Distance:
        """
        Maps UI selection to a Distance domain object.
        Returns:
            Distance: The validated distance object.
        """
        dist_map = {
            "marathon": 42.195,
            "half": 21.0975,
            "10k": 10.0
        }
        
        unit = DistanceUnit(self.distance_unit.get())
        dist_val = dist_map.get(self.distance_type.get(), self.custom_distance.get())
        
        return Distance(dist_val, unit)

    def _handle_calculation(self) -> None:
        """Main orchestrator for the calculation trigger."""
        if not self._validate_all():
            return

        distance = self._get_distance_object()

        try:
            if self.mode.get() == "time_to_pace":
                time_obj = Time.from_hms(self.hours.get(), self.minutes.get(), self.seconds.get())
                pace_obj = self.calculator.time_to_pace(time_obj, distance)
            else:
                pace_seconds = (self.pace_minutes.get() * 60) + self.pace_seconds.get()
                pace_obj = Pace(pace_seconds)
            
            self._update_splits_table(pace_obj, distance)
            
        except ValueError as exc:
            messagebox.showerror("Calculation Error", str(exc))

    def _update_splits_table(self, pace: Pace, distance: Distance) -> None:
        """
        Calculates and renders split times in the Treeview.
        Args:
            pace: The pace to calculate splits for.
            distance: The total distance of the run.
        """
        # Clear table
        for row in self.split_table.get_children():
            self.split_table.delete(row)

        total_km = distance.to_km()
        
        # Whole KM splits
        for km in range(1, int(total_km) + 1):
            time_at_km = Time(int(round(pace.seconds_per_km * km)))
            self.split_table.insert("", "end", values=(f"{km} km", str(time_at_km)))

        # Final fractional split
        if total_km % 1 != 0:
            final_time = Time(int(round(pace.seconds_per_km * total_km)))
            self.split_table.insert("", "end", values=(f"{total_km:.3f} km", str(final_time)))

    def _validate_all(self) -> bool:
        """Aggregated validation logic."""
        try:
            DistanceInputValidator.validate(self.distance_type.get(), self.custom_distance.get())
            
            if self.mode.get() == "time_to_pace":
                TimeInputValidator.validate(self.hours.get(), self.minutes.get(), self.seconds.get())
            else:
                PaceInputValidator.validate(self.pace_minutes.get(), self.pace_seconds.get())
            return True
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return False

    def run(self) -> None:
        """Launch the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = RunningCalculatorApp()
    app.run()