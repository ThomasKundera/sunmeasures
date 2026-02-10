#!/usr/bin/env python3
import logging
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def adjust_contrast(image, saturation_percentile=99):
    """
    Adjust image contrast to ensure ~1% of pixels saturate (255) in at least one channel.

    :param image: Input BGR image (from cv2.imread).
    :param saturation_percentile: Percentile to map to 255 (default: 99 for 1% saturation).
    :return: Contrast-adjusted image.
    """
    # Convert image to float32 for precise calculations
    img_float = image.astype(np.float32)

    # Compute the 99th percentile across all channels
    percentile_value = np.percentile(img_float, saturation_percentile, axis=(0, 1))

    # Scale each channel so the 99th percentile maps to 255
    for channel in range(3):  # R, G, B
        if percentile_value[channel] > 0:  # Avoid division by zero
            scale = 255.0 / percentile_value[channel]
            img_float[:, :, channel] *= scale

    # Clip to [0, 255] and convert back to uint8
    img_adjusted = np.clip(img_float, 0, 255).astype(np.uint8)

    return img_adjusted


def find_sun(image,focal_length,min_radius,max_radius):
    # Adjust contrast for longer focal lengths (>300mm) to enhance
    # Sun brightness
    # FIXME: we may want to do this for shorter focal lengths
    if focal_length > 300:
        image = adjust_contrast(image, saturation_percentile=99)

    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Detect circle with HoughCircles
    circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=60,
        param1=100,
        param2=30,
        minRadius=min_radius,
        maxRadius=max_radius
    )

    # Process and draw the best fit circle
    if circles is not None:
        circles = np.uint16(np.around(circles))
        best_circle = circles[0][0]
        x, y, r = best_circle
        logging.info(f"Circle found: x={x}, y={y}, r={r}, image shape: {gray.shape}, focal_length={focal_length}mm")
    else:
        logging.info(f"No circles found in {imgfile}")
        r=None
    # Draw the circle and center on the original image)
    if (r is not None):
        cv2.circle(image, (x, y), int(r), (0, 255, 0), 3)  # Green circle
        cv2.circle(image, (x, y), 2, (255, 0, 0), 4)  # Red center

    return image,r
