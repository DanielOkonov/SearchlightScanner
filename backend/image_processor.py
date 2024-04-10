from jetson_inference import detectNet
from jetson_utils import (
    cudaToNumpy,
    cudaCrop,
    cudaAllocMapped,
    cudaResize,
)
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

    def detect(self, img_cuda, new_width, new_height, grid_size=None):
        if grid_size is None:
            # Process the whole image
            detections = self.net.Detect(img_cuda, overlay="lines,labels,conf")
        else:
            img_width = img_cuda.width
            img_height = img_cuda.height
            segment_width = img_width // grid_size[0]
            segment_height = img_height // grid_size[1]

            detections = []

            for row in range(grid_size[1]):
                for col in range(grid_size[0]):
                    x1, y1 = col * segment_width, row * segment_height
                    x2, y2 = x1 + segment_width, y1 + segment_height

                    # Crop segment while keeping it in CUDA memory
                    img_segment = cudaAllocMapped(
                        width=segment_width,
                        height=segment_height,
                        format=img_cuda.format,
                    )
                    cudaCrop(img_cuda, img_segment, (x1, y1, x2, y2))

                    # Detect objects in the segment
                    segment_detections = self.net.Detect(
                        img_segment, overlay="lines,labels,conf"
                    )

                    # Adjust detections to full image coordinates
                    for d in segment_detections:
                        d.Left += x1
                        d.Top += y1
                        d.Right += x1
                        d.Bottom += y1
                        detections.append(d)

        # Resize the original image to new dimensions
        # img_resized = cudaAllocMapped(
        #     width=new_width, height=new_height, format=img_cuda.format
        # )
        # cudaResize(img_cuda, img_resized)

        # Convert to numpy array and then to PIL format
        # img_array = cudaToNumpy(img_resized)
        # img_pil = Image.fromarray(img_array)

        # return img_resized, detections
        return detections

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
