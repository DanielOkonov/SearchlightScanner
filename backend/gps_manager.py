from pyembedded.gps_module.gps import GPS
import threading
import time

class GPSManager:
    """
    Class for managing the GPS device in a separate thread, ensuring coordinates are updated only when valid.
    """

    def __init__(self, ports=["/dev/ttyACM0", "COM3"], baud_rate=115200, interval=1):
        """
        Initializer for the GPSManager.
        """
        self.interval = interval
        self.gps = None
        for port in ports:
            try:
                self.gps = GPS(port=port, baud_rate=baud_rate)
                print(f"Connected to GPS on {port}")
                break  # Successfully connected
            except Exception as e:
                print(f"Failed to connect to GPS on {port}: {e}")
                continue

        if self.gps is None:
            raise ValueError("Unable to connect to GPS on any provided port")

        self.running = False
        self.thread = None
        # Initialize latest_coords with a placeholder or default value if you have one
        self.latest_coords = None  

    def start(self):
        """
        Starts the background thread to periodically obtain GPS coordinates.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._update_coordinates)
            self.thread.start()

    def stop(self):
        """
        Stops the background thread.
        """
        self.running = False
        if self.thread:
            self.thread.join()

    def _update_coordinates(self):
        """
        The method running within the thread to periodically update the coordinates.
        """
        while self.running:
            try:
                new_coords = self.gps.get_lat_long()
                if new_coords is not None and new_coords != ('N/A', 'N/A'):  # Update only if new_coords is not None
                    self.latest_coords = new_coords
                    print(f"Updated coordinates: {self.latest_coords}")
            except Exception as e:
                print(f"Unable to get coordinates from GPS: {e}")
            time.sleep(self.interval)

    def get_coords(self):
        """
        Returns the latest valid coordinates obtained by the GPS.
        
        Returns:
            tuple: The latest valid latitude and longitude of the GPS.
            
        Raises:
            ValueError: If the GPS has not obtained any valid coordinates yet.
        """
        if self.latest_coords is None:
            raise ValueError("GPS has not obtained any valid coordinates yet.")
        return self.latest_coords