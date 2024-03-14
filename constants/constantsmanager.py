import os
import json


class ConstantsManager:
    """
    Class to manage constants from a JSON file.
    """

    def __init__(self, filename="values.json"):
        """
        Initializer for ConstantsManager.

        Args:
            filename (str, optional): The filename of the JSON file. Defaults to "values.json".

        Raises:
            FileNotFoundError: If the file does not exist
        """
        self.filename = filename
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"The file '{self.filename}' does not exist.")
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
            The value of the constant

        Raises:
            ValueError: If the key does not exist in the file
        """
        if key in self.constants:
            return self.constants[key]
        else:
            raise ValueError(
                f"The key '{key}' does not exist in the file '{self.filename}'."
            )

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
