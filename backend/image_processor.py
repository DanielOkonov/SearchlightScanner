from jetson_inference import detectNet
from jetson_utils import (cudaToNumpy, cudaFromNumpy)
from .scanner_detection import ScannerDetection
from PIL import Image
import tempfile
import os


class ImageProcessor:
    def __init__(self, model_path=None, labels=None, threshold=0.5):
        labels_path = None
        if labels:
            with tempfile.NamedTemporaryFile(delete=False, mode="w+t") as f:
                labels_path = f.name
                f.writelines([f"{label}\n" for label in labels])
        if model_path:
            self.net = detectNet(model_path, labels_path, threshold)
        else:
            self.net = detectNet("ssd-mobilenet-v2", threshold=threshold)

        if labels_path:
            os.remove(labels_path)

    def detect(self, image, grid_size=None):
        """
        Detect objects in an image.
        Args:
            image (Image): The image to detect objects in.
            grid_size (tuple[int, int], optional): The size of the grid to use for detection. If not provided, the whole image is used.
        Returns:
            list[Detection]: A list of detections.
        """
        detections = []
        if grid_size is not None:
            height, width = image.height, image.width
            grid_height, grid_width = height // grid_size[0], width // grid_size[1]
            image_np = cudaToNumpy(image)
            for i in range(grid_size[0]):
                for j in range(grid_size[1]):
                    start_i, end_i = i * grid_height, (i + 1) * grid_height
                    start_j, end_j = j * grid_width, (j + 1) * grid_width
                    segment = image_np[start_i:end_i, start_j:end_j]
                    segment = cudaFromNumpy(segment)
                    segment_detections = self.net.Detect(segment, overlay="none")
                    for detection in segment_detections:
                        detection.Left += start_j
                        detection.Right += start_j
                        detection.Top += start_i
                        detection.Bottom += start_i
                    detections.extend(segment_detections)
            self.net.Overlay(image, detections, overlay="lines,labels,conf")
        else:
            detections = self.net.Detect(image, overlay="lines,labels,conf")
        return [
            ScannerDetection(self.get_label(detection.ClassID), detection.Confidence)
            for detection in detections
        ]
    
    def get_label(self, label_id):
        """
        Get the label for a given label ID.
        Args:
            label_id (int): The ID of the label to get.
        Returns:
            str: The label for the given ID.
        """
        return self.net.GetClassDesc(label_id)


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
