import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


__all__ = [
    'BBox',
    'crop',
    'mask',
    'crop_and_mask'
]


class BBox:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def to_tuple(self):
        return ((self.xmin, self.ymin), (self.xmax, self.ymax))

    def to_list(self):
        return [[self.xmin, self.ymin], [self.xmax, self.ymax]]


def crop(im, bbox):
    """
    Crops an image to a bounding box

    Parameters
    ----------
    im: input image
        Any number of channels

    bbox: BBox instance
    """
    if len(np.shape(im)) == 3:
        out = im[bbox.ymin:bbox.ymax, bbox.xmin:bbox.xmax, :]
    else:
        out = im[bbox.ymin:bbox.ymax, bbox.xmin:bbox.xmax]
    return out


def mask(im, mask_im, color='black'):
    """
    Masks pixels in an image.

    Pixels in the image that are 1 in the mask are kept.
    Pixels in the image that are 0 in the mask are set to 0.

    Parameters
    ----------
    im: The input image
        Any number of channels

    mask_im: Mask image
        Same height and width as img containing 0 or 1 in each pixel

    color: Color of the mask

    Returns
    -------
    out: The masked image
        Same dimensions and type as img
    """
    out = cv2.bitwise_and(im, im, mask=mask_im)
    if color == 'white':
        add = cv2.cvtColor(~mask_im, cv2.COLOR_GRAY2BGR)
        out = cv2.add(out, add)
    return out


def crop_and_mask(im, bbox, mask_im, mask_color='black'):
    im = mask(im, mask_im, mask_color)
    im = crop(im, bbox)
    return im


class InteractiveCrop:
    """Take an interactive crop of a shape"""

    def __init__(self, im, no_of_sides=1):
        master = tk.Tk()
        self.canvas = tk.Canvas(master, width=im.shape[0], height=im.shape[1])
        self.canvas.pack()
        image = ImageTk.PhotoImage(Image.fromarray(im))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.bind("<Button-1>", self.mouse_callback)
        self.x = []
        self.y = []
        self.points = []
        tk.mainloop()

    def mouse_callback(self, event):
        x = event.x
        y = event.y
        self.update(x, y)

    def update(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.points.append(x)
        self.points.append(y)
        polygon = self.canvas.create_polygon(self.points, outline='black', width=2)