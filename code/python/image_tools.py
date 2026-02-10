#!/usr/bin/env python3
import logging
import cv2
import numpy as np

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