from pyembedded.gps_module.gps import GPS


class GPSManager:
    """
    Class for managing the GPS device.
    This class uses a gps driver and library that was installed onto the os.
    """

    def __init__(self, port="/dev/ttyACM0", baud_rate=9600):
        """
        Initializer for the GPSModule.

        Args:
            port (str, optional): The port the GPS is connected to. Defaults to "/dev/ttyACM0".
            baud_rate (int, optional): The baud rate of the GPS. Defaults to 9600.

        Raises:
            ValueError: If the GPS is unable to connect.
        """
        try:
            self.gps = GPS(port=port, baud_rate=baud_rate)
        except:
            raise ValueError("Unable to connect to GPS")

    def get_coords(self):
        """
        Gets the coordinates from the GPS.

        Returns:
            tuple: The latitude and longitude of the GPS

        Raises:
            ValueError: If the GPS is not connected or if the coordinates are unable to be retrieved.
        """
        if self.gps is None:
            raise ValueError("GPS not connected, connect gps first.")
        else:
            try:
                return self.gps.get_lat_long()
            except:
                raise ValueError("Unable to get coordinates from GPS.")
