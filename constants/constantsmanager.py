import os
import json


class ConstantsManager:
    """
    Class to manage constants from a JSON file.
    """

    BACKUP_JSON_STRING = """
    {
        "default_confidence_level": 25,
        "default_distance": 1,
        "default_resolution": "1920x1080 pixels",
        "default_segmentation": 9,
        "camera_feed_1": "/dev/video0",
        "camera_feed_2": "/dev/video2",
        "gps_name": "/dev/ttyACM0",
        "gps_baud_rate": 115200,
        "led_name": "/dev/ttyUSB0",
        "led_baud_rate": 9600,
        "led_light_duration": 2,
        "image_save_dir": "",
        "image_save_rate": 2,
        "images_per_rate": 1,
        "images_per_dir": 100,
        "image_font_size": 16,
        "image_font_color": "(170, 255, 0)",
        "notes1": "",
        "notes2": "",
        "path_to_model": "",
        "path_to_labels": "",
        "default_targets": {
            "BACKGROUND": "(255, 255, 255)",
            "vehicle": "(34, 177, 76)",
            "ocean debris": "(255, 242, 0)",
            "person": "(163, 73, 164)",
            "powerline": "(255, 174, 201)",
            "dog": "(185, 122, 87)",
            "ship wake": "(136, 0, 21)",
            "airplane": "(237, 28, 36)",
            "helicopter": "(0, 162, 232)",
            "Persons_Thermal": "(63, 72, 204)"
        },
        "selected_targets": {},
        "operator_notes": "",
        "operator_comments": ""
    }
    """

    def __init__(self, filename="default_settings.json"):
        """
        Initializer for ConstantsManager.

        Args:
            filename (str, optional): The filename of the JSON file. Defaults to "values.json".

        Raises:
            FileNotFoundError: If an error occurred while creating the file (if the file does not exist and trying to make a new one)
        """
        self.filename = filename
        if not os.path.isfile(self.filename):
            try:
                print(
                    f"The file '{self.filename}' does not exist. Creating a new one..."
                )
                with open(self.filename, "w") as file:
                    file.write(self.BACKUP_JSON_STRING)
            except Exception as e:
                raise FileNotFoundError(
                    f"An error occurred while creating the file: {e}"
                )
        self.constants = {}
        self.load_constants()

    def load_constants(self):
        """
        Reads the constants from the JSON file.

        Raises:
            ValueError: If the file is not a valid JSON file
            ValueError: If an error occurred while reading the file
        """
        try:
            with open(self.filename, "r") as file:
                self.constants = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"The file '{self.filename}' is not a valid JSON file.")
        except Exception as e:
            raise ValueError(f"An error occurred while reading the file: {e}")

    def get_constant(self, key):
        """
        Gets the value of a constant.

        Args:
            key (str): The key of the constant

        Returns:
            The value of the constant (None if the constant does not exist)

        """
        return self.constants.get(key, None)

    def set_constant(self, key, value):
        """
        Adds or updates a constant in the JSON file.

        Args:
            key (str): The key of the constant
            value (any): The value of the constant

        Raises:
            ValueError: If an error occurred while writing the file
        """
        self.constants[key] = value
        try:
            with open(self.filename, "w") as file:
                json.dump(self.constants, file, indent=4)
        except Exception as e:
            raise ValueError(f"An error occurred while writing the file: {e}")
