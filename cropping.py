import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


__all__ = [
    'BBox',
    'crop',
    'mask',
    'crop_and_mask',
    'crop_circle',
    'crop_polygon'
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


def crop_polygon(im):
    crop_object = CropPolygon(im)
    return crop_object.result


def crop_circle(im):
    crop_object = CropCircle(im)
    return crop_object.result


class CropPolygon:
    """Take an interactive crop of a shape"""

    def __init__(self, im):
        self.im = im
        self.points = []
        self.setup(im)

    def setup(self, im):
        self.master = tk.Tk()
        self.master.wm_title("Crop Polygon")
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        label = tk.Label(self.frame, text="Click to add points to the polygon")
        label.pack()
        self.canvas = tk.Canvas(self.frame, width=im.shape[0], height=im.shape[1])
        self.polygon = self.canvas.create_polygon([0, 0], outline='black', width=2)
        self.canvas.pack()
        image = ImageTk.PhotoImage(Image.fromarray(im))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.bind("<Button-1>", self.mouse1_callback)
        self.canvas.bind("<Button-2>", self.mouse2_callback)
        self.canvas.bind("<Button-3>", self.mouse3_callback)
        self.master.bind("<Return>", self.return_callback)
        undo_button = tk.Button(self.frame, text='Undo (Right Click)', command=self.undo)
        undo_button.pack(side=tk.LEFT, fill=tk.BOTH)
        finished_button = tk.Button(self.frame, text='Finished (Return)', command=self.finish)
        finished_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        reset_button = tk.Button(self.frame, text='Reset (Middle Click)', command=self.reset)
        reset_button.pack(side=tk.LEFT, fill=tk.BOTH)
        tk.mainloop()

    def mouse1_callback(self, event):
        x = event.x
        y = event.y
        self.update(x, y)

    def mouse2_callback(self, event):
        self.reset()

    def mouse3_callback(self, event):
        self.undo()

    def return_callback(self, event):
        self.finish()

    def update(self, x, y):
        self.points.append(x)
        self.points.append(y)
        self.canvas.delete(self.polygon)
        self.polygon = self.canvas.create_polygon(self.points, outline='black', width=2)

    def finish(self):
        points = np.array(self.points)
        points = points.reshape(len(points)//2, 2)
        mask = np.zeros_like(self.im, dtype=np.uint8)
        cv2.fillPoly(mask, pts=np.array([points], dtype=np.int32), color=(255, 255, 255))
        bbox = BBox(min(points[:, 0]), max(points[:, 1]), min(points[:, 1]), max(points[:, 1]))
        self.result = CropResult(bbox, mask, points)
        self.master.quit()

    def reset(self):
        self.points = []
        self.canvas.delete(self.polygon)
        self.polygon = self.canvas.create_polygon([0, 0], outline='black', width=2)

    def undo(self):
        if len(self.points) == 2:
            self.reset()
        elif len(self.points) > 2:
            self.points.pop()
            self.points.pop()
            self.canvas.delete(self.polygon)
            self.polygon = self.canvas.create_polygon(self.points, outline='black', width=2)


class CropCircle:

    def __init__(self, im):
        pass


class CropResult:

    def __init__(self, bbox, mask, points):
        self.bbox = bbox
        self.mask = mask
        self.points = points

    def __str__(self):
        return str(
            "Crop result containing: \n "
            "   bbox: BBox object containing xmin, xmax, ymin, ymax attributes \n"
            "   mask: a mask to apply to an image \n "
            "   points: a list of points ([:, 0] contains x, [:, 1] contains y")