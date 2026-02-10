#!/usr/bin/env python3
import logging
import cv2
import numpy as np
from matplotlib import pyplot as plt
from exifer import ExifData
from image_tools import adjust_contrast
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class SunFit:
    def __init__(self, imgfile):
        logging.info("sun_fit(%s)", imgfile)
        self.imgfile = imgfile
        self.valid=True

    def open_image(self):
        self.image = cv2.imread(self.imgfile)
        if self.image is None:
            logging.error(f"Error: Cannot load image {self.imgfile}")
            self.valid=False

    def run(self):
        self.exif = ExifData(self.imgfile)
        focal_length = self.exif.focal_length
        min_radius = int(self.exif.deg_to_px(0.15))  # Sun is about 0.5 degrees
        max_radius = int(self.exif.deg_to_px(0.35))
        self.open_image()
        if not self.valid:
            return
        # adjust contrast
        adjusted_image = adjust_contrast(self.image)
        # plot image and adjusted image side by side
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(self.image)
        ax2.imshow(adjusted_image)
        plt.show()


def main():
    print("FIXME: standalone tests?")
    return

if __name__ == "__main__":
    main()

