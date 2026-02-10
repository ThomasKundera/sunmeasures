#!/usr/bin/env python3

"""
ExifData class to handle EXIF data and timestamps.
"""
import os
import sys
import logging
import math
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from statistics import mean

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# singleton class for time correction
class TimeFixer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
#            cls._instance.__initialize__()
        return cls._instance

    def initialize(self,workdir):
        # Initialize the TimeFixed instance
        img_list=[
                ("IMG_1448.JPG","7:19:24"),
                ("IMG_1449.JPG","7:19:37"),
                ("IMG_1450.JPG","7:19:38")
        ]
        deltas=[]
        for img in img_list:
            # We don't want to fix time on the ref images!
            exif_data = ExifData(os.path.join(workdir,"data", "time_ref", img[0]),fix_time=False)
            fixed_time = exif_data.date_time.replace(hour=int(img[1].split(":")[0]), 
                                    minute=int(img[1].split(":")[1]), second=int(img[1].split(":")[2]))
            deltas.append(exif_data.date_time - fixed_time)
            print(str(exif_data.date_time - fixed_time)+" "+str(exif_data.date_time)+" "+str(fixed_time))
        self.delta = datetime.timedelta(seconds=mean(delta.total_seconds() for delta in deltas))
        #print("Time delta: "+str(self.delta))

    def fix_time(self, date_time):
        # return date_time - self.delta
        return date_time - self.delta

class ExifData:
    def __init__(self, imgfile,fix_time=True):
        self.imgfile = imgfile
        self.exif_data = None
        self.fix_time = fix_time
        self.read_exif()

    def read_exif(self):
        try:
            self.exif_data = Image.open(self.imgfile)._getexif()
        except Exception as e:
            logging.error(f"Failed to read EXIF for {self.imgfile}: {e}")
            raise
        if self.exif_data is None:
            logging.error(f"No EXIF data for {self.imgfile}")
            raise
 
        # Get datetime
        self.date_time = self.exif_data.get(0x9003)
        if self.date_time:
            try:
                self.date_time = datetime.datetime.strptime(self.date_time, "%Y:%m:%d %H:%M:%S")
                logging.info(f"read_exif({self.imgfile}): Date and time: {self.date_time}")
            except ValueError:
                logging.error(f"Invalid DateTime format in {self.imgfile}")
                raise
        else:
            logging.error(f"No DateTime in EXIF for {self.imgfile}")
            sys.exit(1)

        if self.fix_time:
            time_fixer = TimeFixer()
            self.date_time = time_fixer.fix_time(self.date_time)
        # Get image size
        self.width, self.height = Image.open(self.imgfile).size

        # Get focal length:
        self.focal_length = self.exif_data.get(0x920a, 0)
        if self.focal_length == 0:
            self.focal_length = 1100  # 1000mm f/10 + 13mm extension.

    def px_to_angle(self, r):
        # Canon 550D: Sensor Size 22.3 x 14.9mm
        pxs = 22.3 / self.width
        pys = pxs
        ps = (pxs + pys) / 2
        a = 2 * math.atan2(r * ps, 2 * self.focal_length)  # Diameter in radians
        return a

    def px_to_mn(self, r):
        return 60*math.degrees(self.px_to_angle(r))

    def angle_to_px(self, a):
        """Convert angle  (radians) to pixel size for Canon 550D sensor."""
        pxs = 22.3 / self.width  # Pixel size in mm (x-dimension)
        pys = pxs          # Assume same pixel size for y
        ps = (pxs + pys) / 2  # Average pixel size
        r = (2 * self.focal_length * math.tan(a / 2)) / ps  # Pixel radius
        return r

    def deg_to_px(self,a):
        """Convert angular diameter (degrees) to pixel radius for Canon 550D sensor."""
        return self.angle_to_px(math.radians(a))


def main():
    #TimeFixer()
    #return
    exif_data = ExifData('data/2025_08_22/2000_sun/IMG_1451.JPG')
    print(exif_data.focal_length)
    print(exif_data.width)
    print(exif_data.height)
    print(exif_data.date_time)
    print(exif_data.px_to_angle(1))
    print(exif_data.deg_to_px(0.5))
    
if __name__ == '__main__':
    main()