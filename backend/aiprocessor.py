from jetson_inference import detectNet


class AIProcessor:
    """
    Class for loading and managing AI models
    """

    def __init__(self):
        """
        Initializer for AIProcessor, model is not loaded by default.
        """
        self.net = None

    def load_model(self, model_path, conf_level=0.5):
        """
        Loads an AI model from the specified path.

        Args:
            model_path (str): The path to the AI model
            conf_level (float, optional): The confidence level for the model. Defaults to 0.5.

        Raises:
            ValueError: If the conf_level is not a number
            ValueError: If the conf_level is not between 0 and 1
        """
        if not isinstance(conf_level, (int, float)):
            raise ValueError("conf_level must be a number")
        if not 0 <= conf_level <= 1:
            raise ValueError("conf_level must be between 0 and 1")
        self.net = detectNet(model_path, threshold=conf_level)

    def detect_objects(self, image):
        """
        Detects objects in the given image using the loaded model.

        Args:
            image (unknown): The image to detect objects in

        Raises:
            ValueError: If the model is not loaded

        Returns:
            unknown: The detected objects
        """
        if self.net is None:
            raise ValueError("Model not loaded")
        return self.net.Detect(image)

    def loaded(self):
        """
        Returns whether the model is loaded.

        Returns:
            bool: True if the model is loaded, False otherwise
        """
        return self.net is not None
