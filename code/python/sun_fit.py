#!/usr/bin/env python3
import logging
import cv2
import numpy as np
from matplotlib import pyplot as plt
from exifer import ExifData
from image_tools import find_sun
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
        img,r = find_sun(self.image,focal_length,min_radius,max_radius)
        if r is None:
            logging.error(f"Error: Sun not found in image {self.imgfile}")
            self.valid=False
            return
        self.radius=angle_mn = 2*self.exif.px_to_mn(r)
        self.plot(img)


    def plot(self, img):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6)) 

        ax1.imshow(self.image)
        ax1.set_title("Original")
        ax1.axis('off')

        ax2.imshow(img)
        ax2.set_title("Processed")
        ax2.axis('off')

        text = f"Radius: {self.radius:.1f} '"
        ax2.text(
            x=0.98,                        # 98% from left → near right edge
            y=0.02,                        # 2% from bottom → near bottom
            s=text,
            color='white',
            fontsize=14,
            fontweight='bold',
            ha='right',                    # horizontal alignment: right
            va='bottom',                   # vertical alignment: bottom
            transform=ax2.transAxes,       # very important: coordinates in axes fraction (0–1)
            bbox=dict(                     # optional: nice background box
                facecolor='black',
                alpha=0.6,
                edgecolor='none',
                boxstyle='round,pad=0.3'
            )
        )

        plt.tight_layout()
        plt.show()

def main():
    print("FIXME: standalone tests?")
    return

if __name__ == "__main__":
    main()

