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
