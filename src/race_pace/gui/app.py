import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from race_pace.services.calculator import CalculatorService
from race_pace.domain.pace import Pace
from race_pace.domain.time import Time
from race_pace.validation.time_validation import TimeInputValidator
from race_pace.validation.distance_validation import DistanceInputValidator
from race_pace.validation.pace_validation import PaceInputValidator
from race_pace.domain.distance import Distance, DistanceUnit


class RunningCalculatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Running Calculator")

        self.calculator = CalculatorService()

        self._create_variables()
        self._create_layout()
    
    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def _get_distance(self) -> Distance:
        distance_type = self.distance_type.get()
        unit = DistanceUnit(self.distance_unit.get())

        if distance_type == "marathon":
            return Distance(42.195, unit)
        elif distance_type == "half":
            return Distance(21.0975, unit)
        elif distance_type == "10k":
            return Distance(10.0, unit)
        else:
            return Distance(self.custom_distance.get(), unit)

    def _update_mode(self):
        """Update input frames based on selected mode."""
        # Destroy old input frame if it exists
        if hasattr(self, "_input_frame") and self._input_frame:
            self._input_frame.destroy()

        # Recreate the appropriate input frame
        if self.mode.get() == "time_to_pace":
            self._input_frame = self._create_time_frame(self.root)
        else:
            self._input_frame = self._create_pace_frame(self.root)

    def _create_variables(self):
        self.mode = tk.StringVar(value="time_to_pace")

        self.distance_type = tk.StringVar(value="marathon")
        self.custom_distance = tk.DoubleVar(value=10.0)
        self.distance_unit = tk.StringVar(value="km")
        
        self.hours = tk.IntVar(value=3)
        self.minutes = tk.IntVar(value=0)
        self.seconds = tk.IntVar(value=0)
        
        self.pace_minutes = tk.IntVar(value=5)
        self.pace_seconds = tk.IntVar(value=0)
        
        self.include_half = tk.BooleanVar(value=True)

    def _create_layout(self):
        self._create_mode_frame(self.root)
        self._create_distance_frame(self.root)
        
        # Create the input frame dynamically via _update_mode
        self._input_frame = None
        self._update_mode()

        self._create_action_frame(self.root)
        self._create_split_frame(self.root)
    
    def _create_mode_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Calculation Mode")
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        ttk.Radiobutton(
            frame,
            text="Finish Time → Pace",
            variable=self.mode,
            value="time_to_pace",
            command=self._update_mode
        ).grid(row=0, column=0, sticky="w")

        ttk.Radiobutton(
            frame,
            text="Pace → Finish Time",
            variable=self.mode,
            value="pace_to_time",
            command=self._update_mode
        ).grid(row=0, column=1, sticky="w")

        return frame
    
    # Mode selection frame
    def _create_distance_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Distance")
        frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        ttk.Combobox(
            frame,
            textvariable=self.distance_type,
            values=["marathon", "half", "10k", "custom"],
            state="readonly"
        ).grid(row=0, column=0)

        ttk.Entry(
        frame,
        textvariable=self.custom_distance,
        width=8
        ).grid(row=0, column=1)

        ttk.Combobox(
            frame,
            textvariable=self.distance_unit,
            values=["km", "miles"],
            state="readonly",
            width=8
        ).grid(row=0, column=2)

        return frame

    # Distance input frame
    def _create_time_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Finish Time")
        frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        ttk.Label(frame, text="Time (h:m:s)").grid(row=0, column=0)
        ttk.Spinbox(frame, from_=0, to=23, textvariable=self.hours, width=5).grid(row=0, column=0)
        
        ttk.Label(frame, text=":").grid(row=0, column=1)
        ttk.Spinbox(frame, from_=0, to=59, textvariable=self.minutes, width=5).grid(row=0, column=2)
        ttk.Label(frame, text=":").grid(row=0, column=3)
        ttk.Spinbox(frame, from_=0, to=59, textvariable=self.seconds, width=5).grid(row=0, column=4)

        return frame
    
    # Time and pace input frame
    def _create_pace_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Input")
        frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        ttk.Label(frame, text="Time (h:m:s)").grid(row=0, column=0)
        ttk.Spinbox(frame, from_=0, to=23, textvariable=self.hours, width=5).grid(row=0, column=1)
        ttk.Spinbox(frame, from_=0, to=59, textvariable=self.minutes, width=5).grid(row=0, column=2)
        ttk.Spinbox(frame, from_=0, to=59, textvariable=self.seconds, width=5).grid(row=0, column=3)

        ttk.Label(frame, text="Pace (min/km)").grid(row=1, column=0)
        ttk.Spinbox(frame, from_=0, to=20, textvariable=self.pace_minutes, width=5).grid(row=1, column=1)
        ttk.Spinbox(frame, from_=0, to=59, textvariable=self.pace_seconds, width=5).grid(row=1, column=2)

        return frame
    
    # Calculate button
    def _create_action_frame(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(
            frame,
            text="Calculate",
            command=self._calculate
        ).grid(row=0, column=0)

        return frame

    # Calculation handler
    def _calculate(self):
        if not self._validate_inputs():
            return

        distance = self._get_distance()

        try:
            if self.mode.get() == "time_to_pace":
                time = Time.from_hms(
                    self.hours.get(),
                    self.minutes.get(),
                    self.seconds.get()
                )
                pace = self.calculator.time_to_pace(time, distance)
            else:
                pace = Pace(self.pace_minutes.get() * 60 + self.pace_seconds.get())
                time = self.calculator.pace_to_time(pace, distance)

        except ValueError as exc:
            messagebox.showerror("Calculation error", str(exc))
            return

        self._update_splits(pace, distance)


    # Split Table
    def _create_split_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Splits")
        frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

        self.split_table = ttk.Treeview(
            frame,
            columns=("distance", "time"),
            show="headings"
        )
        self.split_table.heading("distance", text="Distance (km)")
        self.split_table.heading("time", text="Cumulative Time")
        self.split_table.pack(fill="both", expand=True)

        return frame

    def _validate_inputs(self) -> bool:
        try:
            DistanceInputValidator.validate(
                self.distance_type.get(),
                self.custom_distance.get()
            )

            if self.mode.get() == "time_to_pace":
                TimeInputValidator.validate(
                    self.hours.get(),
                    self.minutes.get(),
                    self.seconds.get()
                )
            else:
                PaceInputValidator.validate(
                    self.pace_minutes.get(),
                    self.pace_seconds.get()
                )

        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return False

        return True