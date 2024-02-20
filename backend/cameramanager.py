from jetson_utils import videoSource


class CameraManager:
    """
    Class for managing the camera.
    This classes using the videoSource class from jetson_utils, CV2 can also be used.
    """

    def __init__(self):
        """
        Initializer for CameraManager, input is not open by default.
        """
        self.input = None

    def open(self, uri, argv=None):
        """
        Opens the camera with the specified URI.

        Args:
            uri (str): The URI of the camera
            argv (list, optional): The arguments to pass to the camera. Defaults to None.

        Raises:
            ValueError: If the camera is already open
            ValueError: If the camera fails to open
        """
        if self.input is not None:
            raise ValueError("Camera already open")
        try:
            self.input = videoSource(uri, argv=argv)
            self.input.Open()
        except Exception as e:
            raise ValueError(f"Failed to open video source {uri}: {e}") from e

    def fetch_frame(self):
        """
        Fetches a frame from the camera.

        Raises:
            ValueError: If the camera is not open
        """
        if self.input is None:
            raise ValueError("Camera not open, open camera before fetching frame")
        return self.input.Capture()

    def close(self):
        """
        Closes the camera.

        Raises:
            ValueError: If the camera is not open
        """
        if self.input is None:
            raise ValueError("Camera not open, open camera before closing")
        self.input.Close()
        self.input = None
