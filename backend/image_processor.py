from jetson_inference import detectNet
from jetson_utils import (cudaToNumpy, cudaFromNumpy)
from .scanner_detection import ScannerDetection
from PIL import Image
import tempfile
import os
from frontend.shared_labels_controller import shared_labels


class ImageProcessor:

    def __init__(self, model_path=None):
        self.model_path = model_path
        self.detect_net = None
        self.update_labels(init=True)

    def update_labels(self, init=False):
        if init:
            labels_and_colors = shared_labels.get_init_labels()  
        else:
            labels_and_colors = shared_labels.get_label_color() 
        
        labels = [label for label, _ in labels_and_colors]
        colors = [color for _, color in labels_and_colors]

        temp_label_file = tempfile.NamedTemporaryFile(delete=False)
        temp_color_file = tempfile.NamedTemporaryFile(delete=False)

        try:
            with open(temp_label_file.name, 'w') as f:
                for label in labels:
                    f.write(label + '\n')

            with open(temp_color_file.name, 'w') as f:
                for color in colors:
                    f.write(str(color) + '\n')

            model = self.model_path if self.model_path else "ssd-mobilenet-v2"
            threshold = 0.5

            if model == "ssd-mobilenet-v2":
                self.net = detectNet("ssd-mobilenet-v2", threshold=threshold)
            else:
                self.net = detectNet(model=model, labels=temp_label_file.name, colors=temp_color_file.name, threshold=threshold, input_blob="input_0", output_cvg="scores", output_bbox="boxes")

        finally:
            os.unlink(temp_label_file.name)  
            os.unlink(temp_color_file.name)  

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
            detections = [detection for detection in detections if self.get_label(detection.ClassID) != 'void']
            self.net.Overlay(image, detections, overlay="lines,labels,conf")
        else:
            detections = self.net.Detect(image, overlay="none")
            detections = [detection for detection in detections if self.get_label(detection.ClassID) != 'void']
            self.net.Overlay(image, detections, overlay="lines,labels,conf")
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
