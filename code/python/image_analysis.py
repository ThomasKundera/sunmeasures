#!/usr/bin/env python3
import logging
import os
from multiprocessing import Pool, cpu_count
from functools import partial
from matplotlib import pyplot as plt
from exifer import TimeFixer
from sun_fit import SunFit

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

kBatch = "2025_08_22"  # Batch date
kRSD = 2001

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
                'diameter': sun_fit.diameter
            }
            logging.info("Finished image: %s", img)
            return result
        except:
            logging.info("Error processing image: %s: ", img)
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

    def plot(self):
        logging.info("plot: Start")
        if not self.results:
            logging.warning("No valid images found")
            return

        times_of_day = []
        diameters = []

        for res in self.results:
            dt = res['datetime']           # datetime object
            tod = dt.time()                # time object (hour, min, sec)
            
            # Convert to decimal hours
            hours_decimal = tod.hour + tod.minute / 60 + tod.second / 3600
            
            times_of_day.append(hours_decimal)
            diameters.append(res['diameter'])
        
        fig, ax = plt.subplots(figsize=(11, 6))
        # Scatter plot
        ax.scatter(times_of_day, diameters,
                   s=60,               # point size
                   alpha=0.7,
                   color='royalblue',
                   edgecolor='navy',
                   linewidth=0.5,
                   label='Measured solar diameter')
        
        # Format plot
        ax.set_title('Measured solar diameter over time')
        ax.set_xlim(6, 21)
        ax.set_ylim(20, 40)
        ax.set_xticks(range(6, 21, 2))
        ax.set_xticklabels([f"{h:02d}:00" for h in range(6, 21, 2)])
        ax.set_xlabel("Time of day", fontsize=12)
        ax.set_ylabel("Solar diameter [arcminutes]", fontsize=12)
        ax.set_title("Measured solar diameter vs time of day", fontsize=14, pad=12)

        # Grid
        ax.grid(True, linestyle='--', alpha=0.5, axis='both')
        ax.axhline(31.0, color='darkred', linestyle='--', alpha=0.6,
                   label="Nominal solar diameter ≈ 31′")
        ax.legend(loc='upper right', fontsize=10)

        # ── Add sunrise & sunset vertical lines ─────────────
        sunrise_hour = 6 + 50/60      # 6:50 → ~6.833
        sunset_hour  = 20 + 13/60      # 20:13 → ~20.217

        ax.axvline(x=sunrise_hour, color='gold', linestyle='--', linewidth=2.2,
                label='Sunrise (approx. 06:50)', alpha=0.9)

        ax.axvline(x=sunset_hour, color='darkorange', linestyle='--', linewidth=2.2,
                label='Sunset (approx. 20:13)', alpha=0.9)

        plt.tight_layout()
        plt.show()
        logging.info("plot: End")


def main():
    logging.info("main: Start")
    logging.info("kWORKDIR: %s", kWORKDIR)
    logging.info("kPROJECTDIR: %s", kPROJECTDIR)
    # Set up time fixer
    time_fixer = TimeFixer()
    time_fixer.initialize(kPROJECTDIR)
    analysis=Analysis()
    analysis.run()
    analysis.plot()
    logging.info("main: End")

if __name__ == "__main__":
    main()
