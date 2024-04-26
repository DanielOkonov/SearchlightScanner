import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from constantsmanager import ConstantsManager

segmentation_options = [
    {
        "text": "1 segment",
        "value": 1,
    },
    {
        "text": "4 segments",
        "value": 4,
    },
    {
        "text": "9 segments",
        "value": 9,
    },
    {
        "text": "16 segments",
        "value": 16,
    },
    {
        "text": "25 segments",
        "value": 25,
    },
    {
        "text": "40 segments",
        "value": 40,
    },
    {
        "text": "50 segments",
        "value": 60,
    },
    {
        "text": "84 segments",
        "value": 84,
    },
]

resolution_options = [
    {
        "text": "280x720 pixels",
        "value": "280x720",
    },
    {
        "text": "1920x1080 pixels",
        "value": "1920x1080",
    },
    {
        "text": "2560x1440 pixels",
        "value": "2560x1440",
    },
    {
        "text": "3840x2160 pixels",
        "value": "3840x2160",
    },
]


def get_segmentation_value(text):
    for option in segmentation_options:
        if option["text"] == text:
            return option["value"]
    return None  # Return None if text is not found


def get_resolution_value(text):
    for option in resolution_options:
        if option["text"] == text:
            return option["value"]
    return None  # Return None if text is not found


def read_csv_and_convert_to_json(csv_file_path):
    data = []
    with open(csv_file_path, newline="") as csvfile:
        for line in csvfile:
            category, color = line.strip().split(",")
            data.append({"target": category, "color": color.upper()})
    return data


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Constants")
        self.configure(bg="#7C889C")
        self.geometry("600x400")

        # Instance variables to store values
        # settings 1
        self.default_confidence_level = tk.IntVar(value=90)
        self.default_distance = tk.IntVar(value=0)
        self.default_resolution = tk.StringVar(value="280x720 pixels")

        # settings 2
        self.default_segmentation = tk.StringVar(value="1 segment")

        # paths
        self.default_model_path = tk.StringVar(value="")
        self.default_labels_path = tk.StringVar(value="")

        self.create_form()

    def on_close(self):
        self.destroy()

    def browse_model(self):
        model_path = filedialog.askopenfilename(
            filetypes=[("ONYX files", "*.onyx"), ("All files", "*.*")]
        )
        if model_path:
            self.default_model_path.set(model_path)

    def browse_labels(self):
        labels_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if labels_path:
            self.default_labels_path.set(labels_path)

    def validate_numeric_input(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def update_confidence_level(self, event):
        value = self.confidence_level_entry.get()
        if self.validate_numeric_input(value):
            int_value = int(value)
            if int_value > 100 or int_value < 0:
                self.confidence_level_entry.delete(0, tk.END)
            else:
                self.default_confidence_level.set(int_value)
        else:
            self.confidence_level_entry.delete(0, tk.END)

    def update_distance(self, event):
        value = self.default_distance_entry.get()
        if self.validate_numeric_input(value):
            int_value = int(value)
            if int_value > 100:
                self.default_distance_entry.delete(0, tk.END)
            self.default_distance.set(int(value))
        else:
            self.default_distance_entry.delete(0, tk.END)

    def update_segmentation(self, event):
        self.default_segmentation.set(self.segmentation_entry.get())

    def update_resolution(self, event):
        self.default_resolution.set(self.resolution_entry.get())

    def save_constants(self):
        default_targets = read_csv_and_convert_to_json(self.default_labels_path.get())

        constants_manager = ConstantsManager()
        constants_manager.set_constant(
            "default_confidence_level", self.default_confidence_level.get()
        )
        constants_manager.set_constant("default_distance", self.default_distance.get())
        constants_manager.set_constant(
            "default_resolution", get_resolution_value(self.default_resolution.get())
        )
        constants_manager.set_constant(
            "default_segmentation",
            get_segmentation_value(self.default_segmentation.get()),
        )
        constants_manager.set_constant("path_to_model", self.default_model_path.get())
        constants_manager.set_constant("path_to_labels", self.default_labels_path.get())
        constants_manager.set_constant("default_targets", default_targets)
        print("Constants saved successfully!")

    def create_form(self):
        row = 0
        root_label = tk.Label(
            self,
            text="Constants:",
            font=("Arial", 14, "bold"),
            bg="#7C889C",
            fg="white",
        )
        root_label.pack(pady=(10, 5))

        form_frame = tk.Frame(self, bg="#7C889C")
        form_frame.pack(pady=(0, 10))

        # Default Confidence Level
        confidence_level_label = tk.Label(
            form_frame, text="Default Confidence Level:", bg="#7C889C", fg="white"
        )
        confidence_level_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.confidence_level_entry = tk.Entry(
            form_frame, textvariable=self.default_confidence_level
        )
        self.confidence_level_entry.grid(row=row, column=1, padx=10, pady=5)
        self.confidence_level_entry.bind("<KeyRelease>", self.update_confidence_level)
        self.confidence_level_entry.config(validate="key")
        self.confidence_level_entry["validatecommand"] = (
            self.confidence_level_entry.register(self.validate_numeric_input),
            "%P",
        )
        row += 1

        # Defult distance
        distance_label = tk.Label(
            form_frame, text="Default Distance:", bg="#7C889C", fg="white"
        )
        distance_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.default_distance_entry = tk.Entry(
            form_frame, textvariable=self.default_distance
        )
        self.default_distance_entry.grid(row=row, column=1, padx=10, pady=5)
        self.confidence_level_entry.bind("<KeyRelease>", self.update_distance)
        self.default_distance_entry.config(validate="key")
        self.default_distance_entry["validatecommand"] = (
            self.default_distance_entry.register(self.validate_numeric_input),
            "%P",
        )
        row += 1

        # Default Resolution
        resolution_label = tk.Label(
            form_frame, text="Default Resolution:", bg="#7C889C", fg="white"
        )
        resolution_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.resolution_entry = ttk.Combobox(
            form_frame,
            values=[option["text"] for option in resolution_options],
            textvariable=self.default_resolution,
        )
        self.resolution_entry.grid(row=row, column=1, padx=10, pady=5)
        self.resolution_entry.bind("<<ComboboxSelected>>", self.update_resolution)
        row += 1

        # Default Segmentation (Single-select)
        segmentation_label = tk.Label(
            form_frame, text="Default Segmentation:", bg="#7C889C", fg="white"
        )
        segmentation_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.segmentation_entry = ttk.Combobox(
            form_frame,
            values=[option["text"] for option in segmentation_options],
            textvariable=self.default_segmentation,
        )
        self.segmentation_entry.grid(row=row, column=1, padx=10, pady=5)
        self.segmentation_entry.bind("<<ComboboxSelected>>", self.update_segmentation)
        row += 1

        # Model Frame
        model_frame = tk.Frame(form_frame, bg="#7C889C")
        model_frame.grid(row=row, columnspan=2, pady=(10, 5))

        path_to_model_label = tk.Label(
            model_frame, text="Path to Model:", bg="#7C889C", fg="white"
        )
        path_to_model_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.model_entry = tk.Entry(
            model_frame, width=30, textvariable=self.default_model_path
        )
        self.model_entry.grid(row=0, column=1, padx=10, pady=5)
        browse_model_button = tk.Button(
            model_frame, text="Browse", command=self.browse_model
        )
        browse_model_button.grid(row=0, column=2, padx=5, pady=5)
        row += 1

        # Labels Frame
        labels_frame = tk.Frame(form_frame, bg="#7C889C")
        labels_frame.grid(row=row, columnspan=2, pady=(5, 10))

        path_to_label_file_label = tk.Label(
            labels_frame, text="Path to Labels File:", bg="#7C889C", fg="white"
        )
        path_to_label_file_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.labels_entry = tk.Entry(
            labels_frame, width=30, textvariable=self.default_labels_path
        )
        self.labels_entry.grid(row=0, column=1, padx=10, pady=5)
        browse_labels_button = tk.Button(
            labels_frame, text="Browse", command=self.browse_labels
        )
        browse_labels_button.grid(row=0, column=2, padx=5, pady=5)
        row += 1

        # Save Button
        save_button = tk.Button(
            self,
            text="Save",
            bg="#4CAF50",  # Green color for highlighting
            fg="white",
            font=("Arial", 12),
            command=self.save_constants,
            width=10,  # Adjust the width as needed
            height=2,  # Adjust the height as needed
            relief=tk.RAISED,  # Add a raised border
        )
        save_button.pack(pady=(10, 20))


if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Ensure clean exit
    app.mainloop()
