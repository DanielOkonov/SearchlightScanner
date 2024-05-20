from jetson_utils import videoSource


class CameraManager:
    """
    Class for managing the camera.
    This classes using the videoSource class from jetson_utils, CV2 can also be used.
    """

    def __init__(self, source, width, height):
        """
        Initializer for CameraManager, input is not open by default.
        """
        self.source = videoSource(
            source,
            argv=["--input-width={}".format(width), "--input-height={}".format(height)],
        )
        self.source_name = source
        self.width = width
        self.height = height
    
    def change_camera(self, source):
        """
        Change the camera source.

        Args:
            source (str): New camera source.
        """
        self.source.Close()
        self.source = videoSource(
            source,
            argv=["--input-width={}".format(self.width), "--input-height={}".format(self.height)],
        )
        self.source_name = source

    def change_resolution(self, width, height):
        """
        Change the resolution of the camera.

        Args:
            width (int): New width.
            height (int): New height.
        """
        self.width = width
        self.height = height
        self.source.Close()
        self.source = videoSource(
            self.source_name,
            argv=["--input-width={}".format(width), "--input-height={}".format(height)],
        )

    def capture(self):
        """
        Capture an image from the camera.

        Returns:
            CUDA Image: Image from the camera.
        """
        return self.source.Capture()

    def getFPS(self):
        """
        Get the FPS of the camera.

        Returns:
            int: FPS of the camera.
        """
        return self.source.GetFrameRate()

    def release(self):
        """
        Release the camera.
        """
        self.source.Close()
        self.source = None
