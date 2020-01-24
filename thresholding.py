import cv2
import numpy as np


__all__ = [
   'threshold',
    'adaptive_threshold'
]


def threshold(im, value=None, mode=cv2.THRESH_BINARY):
    """
    Thresholds an image

    Pixels below thresh set to black, pixels above set to white
    """
    if value is None:
        mode = mode + cv2.THRESH_OTSU
    return cv2.threshold(im, value, 255, mode)[1]


def adaptive_threshold(im, block_size, constant, mode=cv2.THRESH_BINARY):
    """
    Performs an adaptive threshold on an image

    Uses cv2.ADAPTIVE_THRESH_GAUSSIAN_C:
        threshold value is the weighted sum of neighbourhood values where
        weights are a gaussian window.

    Uses cv2.THRESH_BINARY:
        Pixels below the threshold set to black
        Pixels above the threshold set to white

    Parameters
    ----------
    img: numpy array containing an image

    block_size: the size of the neighbourhood area

    constant: subtracted from the weighted sum
    """
    out = cv2.adaptiveThreshold(
        im,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        mode,
        block_size,
        constant
    )
    return out


# TODO: Add inrange
# TODO: Add watershed
# TODO: Add distance transform