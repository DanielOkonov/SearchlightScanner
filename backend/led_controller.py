import serial
import time
import threading

class LEDController:
    def __init__(self):
        self.com_port = '/dev/ttyUSB0'
        self.baud_rate = 9600
        try:
            self.serial = serial.Serial(self.com_port, self.baud_rate, timeout=1)
        except Exception as e:
            # print(f"Error: {str(e)}")
            self.serial = None

    def flash_led(self, duration=1):
        """Flashes the LED for a given duration in seconds."""
        # Start the flashing in a new thread
        thread = threading.Thread(target=self._flash_led_worker, args=(duration,))
        thread.start()

    def _flash_led_worker(self, duration):
        """Worker method to flash LED without blocking the main program."""
        if self.serial is None:
            # print("Error: Serial port not open")
            return
        try:
            self.serial.write(b"AT+CH1=1")  # Turn LED on
            time.sleep(duration)           # Keep LED on for the duration
            self.serial.write(b"AT+CH1=0")  # Turn LED off
        except Exception as e:
            pass
            # print(f"Error: {str(e)}")     

    def close(self):
        self.serial.close()  # Close serial port