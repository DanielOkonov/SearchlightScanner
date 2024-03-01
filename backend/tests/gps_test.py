import sys

sys.path.append("/jetson-inference/data/SearchlightScanner/backend")
from gps_module import GPSModule
import time


def main():
    gps = GPSModule()
    while True:
        start_time = time.time()
        coords = gps.get_coords()
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Coordinates: {coords}, Time Taken: {time_taken:.6f} seconds")


if __name__ == "__main__":
    main()
