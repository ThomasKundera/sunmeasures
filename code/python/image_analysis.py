#!/usr/bin/env python3
import logging
import os

from exifer import TimeFixer
from sun_fit import SunFit

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

kBatch = "2025_08_22"  # Batch date
kRSD = 2000

kWORKDIR=os.environ.get('WORKDIR')
kPROJECTDIR=os.environ.get('PROJECTDIR')

class Analysis:
    def __init__(self):
        self.latitude = 43.7  # Nice, France
        self.longitude = 7.3
        self.imgdir = os.path.join(kPROJECTDIR,'data', kBatch, str(kRSD) + '_sun')
        self.disk_out_dir = os.path.join(kWORKDIR, kBatch, 'disk_out')
        logging.info("disk_out_dir: %s", self.disk_out_dir)
        os.makedirs(self.disk_out_dir, exist_ok=True)

    def for_one_image(self, img):
        logging.info("Processing image: %s", img)
        imgfile = os.path.join(self.imgdir, img)
        sun_fit=SunFit(imgfile)
        sun_fit.run()
        return

    def run(self):
        data=[]
        idx=0
        for img in sorted(os.listdir(self.imgdir)):
            result = self.for_one_image(img)

def main():
    logging.info("main: Start")
    logging.info("kWORKDIR: %s", kWORKDIR)
    logging.info("kPROJECTDIR: %s", kPROJECTDIR)
    # Set up time fixer
    time_fixer = TimeFixer()
    time_fixer.initialize(kPROJECTDIR)
    analysis=Analysis()
    analysis.run()
    logging.info("main: End")

if __name__ == "__main__":
    main()
