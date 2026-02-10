#!/usr/bin/env python3
import logging
import os
from multiprocessing import Pool, cpu_count
from functools import partial

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
        self.results = []

    def for_one_image(self, img):
        try:
            logging.info("Processing image: %s", img)
            imgfile = os.path.join(self.imgdir, img)
            sun_fit=SunFit(imgfile)
            sun_fit.run()
            if sun_fit.valid == False:
                logging.info("Invalid image: %s", img)
                return None
            result = {
                'datetime': sun_fit.exif.date_time,
                'radius': sun_fit.radius
            }

            logging.info("Finished image: %s", img)
        except:
            logging.info("Error processing image: %s: %s", img, e)
            return None

    def run(self):
        # Get all image files
        images = sorted([f for f in os.listdir(self.imgdir) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

        if not images:
            logging.warning("No images found in %s", self.imgdir)
            return

        logging.info(f"Found {len(images)} images to process")
        num_processes = max(1, cpu_count() - 1)
        with Pool(processes=num_processes) as pool:
            results = pool.map(self.for_one_image, images)
            self.results = [r for r in results if r is not None]

        logging.info(f"Found {len(self.results)} valid images")

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
