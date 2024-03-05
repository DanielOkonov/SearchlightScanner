from jetson_inference import detectNet
from jetson_utils import cudaImage, cudaToNumpy, cudaFromNumpy


class AIProcessor:
    """
    Class for loading and managing AI models for object detection.
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
            ValueError: If the conf_level is not between 0 and 1
            ValueError: If there is an error loading the model
        """
        if not 0 <= conf_level <= 1:
            raise ValueError("conf_level must be between 0 and 1")
        try:
            self.net = detectNet(model_path, threshold=conf_level)
        except:
            raise ValueError("Error loading model")

    def detect_objects(self, image, grid_size=None):
        """
        Detects objects in the given image using the loaded model.

        Args:
            image (cudaImage): The image to detect objects in
            grid_size (tuple, optional): The grid size to segment the image. If None, the image won't be segmented. Defaults to None.

        Raises:
            ValueError: If the model is not loaded
            ValueError: If there is an error detecting objects

        Returns:
            list[Detection]: A list of detected objects
        """
        if self.net is None:
            raise ValueError("Model not loaded")

        if not isinstance(image, cudaImage):
            raise ValueError("Image must be a cudaImage when using segmentation")

        try:
            if grid_size is not None:
                height, width = image.height, image.width
                grid_height, grid_width = height // grid_size[0], width // grid_size[1]

                image_np = cudaToNumpy(image)
                detections = []

                for i in range(grid_size[0]):
                    for j in range(grid_size[1]):
                        start_i, end_i = i * grid_height, (i + 1) * grid_height
                        start_j, end_j = j * grid_width, (j + 1) * grid_width
                        segment = image_np[start_i:end_i, start_j:end_j]
                        segment = cudaFromNumpy(segment)
                        segment_detections = self.net.Detect(segment)
                        detections.extend(segment_detections)
                return detections

            else:
                return self.net.Detect(image)
        except:
            raise ValueError("Error detecting objects")

    def set_confidence(self, conf_level):
        """
        Sets the confidence level for the model.

        Args:
            conf_level (float): The confidence level for the model

        Raises:
            ValueError: If the model is not loaded
            ValueError: If the conf_level is not between 0 and 1
            ValueError: If there is an error setting the confidence level
        """
        if self.net is None:
            raise ValueError("Model not loaded")
        if not 0 <= conf_level <= 1:
            raise ValueError("conf_level must be between 0 and 1")
        try:
            self.net.SetConfidenceThreshold(conf_level)
        except:
            raise ValueError("Error setting confidence level")

    def set_threshold(self, threshold):
        """
        Sets the threshold for the model.

        Args:
            threshold (float): The threshold for the model

        Raises:
            ValueError: If the model is not loaded
            ValueError: If the threshold is not between 0 and 1
            ValueError: If there is an error setting the threshold
        """
        if self.net is None:
            raise ValueError("Model not loaded")
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")
        try:
            self.net.SetThreshold(threshold)
        except:
            raise ValueError("Error setting threshold")

    def loaded(self):
        """
        Returns whether the model is loaded.

        Returns:
            bool: True if the model is loaded, False otherwise
        """
        return self.net is not None
