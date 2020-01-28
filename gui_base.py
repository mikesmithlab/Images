import tkinter as tk
import random
from PIL import Image, ImageTk
from __init__ import *
import numpy as np


__all__ = [
    "ParamGui"
]


class ParamGui:

    def __init__(self, img_or_vid):
        self._file_setup(img_or_vid)
        self.im0 = self.im.copy()
        self.width, self.height = self.im.shape[:2]
        self.init_ui()

    def _file_setup(self, img_or_vid):
        if isinstance(img_or_vid, np.ndarray):
            if self.grayscale:
                self.im = bgr_to_gray(img_or_vid)
            else:
                self.im = img_or_vid
            self.type = 'singleframe'
        else:
            self.read_vid = img_or_vid
            self.frame_no = 0
            self.num_frames = self.read_vid.num_frames
            self.read_vid.grayscale = self.grayscale
            self.im = self.read_vid.find_frame(self.frame_no)
            self.type = 'multiframe'

    def init_ui(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height)

        image = ImageTk.PhotoImage(Image.fromarray(self.im))
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.image = image
        self.canvas.pack()

        # Create live update checkbox
        self.live_update = tk.BooleanVar(False)
        cb = tk.Checkbutton(self.frame, text='Live update', variable=self.live_update, onvalue=True, offvalue=False, command=self.cb_callback)
        cb.pack()

        self.add_sliders()

        tk.mainloop()

    def cb_callback(self):
        if self.live_update:
            self._update_sliders()

    def slider_callback(self, val):
        if self.live_update.get():
            self._update_sliders()

    def add_sliders(self):

        self.sliders = {}
        self.labels = {}

        if self.type == 'multiframe':
            frame = tk.Frame(self.frame)
            label = tk.Label(frame, text='frame')
            label.pack(side=tk.LEFT)
            self.frame_slider = tk.Scale(frame, from_=0, to=self.num_frames, orient=tk.HORIZONTAL, length=self.width//2, command=self.slider_callback)
            self.frame_slider.pack(side=tk.LEFT, fill=tk.X)

        for key in sorted(self.param_dict.keys()):
            params = self.param_dict[key]
            val, bottom, top, step = params
            frame = tk.Frame(self.frame)
            label = tk.Label(frame, text=key)
            label.pack(side=tk.LEFT)
            var = tk.Variable(value=val)
            slider = tk.Scale(frame, from_=bottom, to=top, resolution=step, orient=tk.HORIZONTAL, length=self.width//2, command=self.slider_callback, variable=var)
            # slider.set(val)
            slider.pack(side=tk.LEFT, fill=tk.X)
            frame.pack()
            self.sliders[key] = slider

    def _update_sliders(self):
        if self.type == 'multiframe':
            self.frame_no = self.frame_slider.get()
            self.im0 = self.read_vid.find_frame(self.frame_no)

        for key in self.param_dict:
            val = self.sliders[key].get()
            self.param_dict[key][0] = val
        self.update()
        self.update_im()

    def update(self):
        self.im = ~self.im

    def update_im(self):
        self.image = ImageTk.PhotoImage(Image.fromarray(self.im))
        self.canvas.itemconfig(self.canvas_image, image=self.image)

    def _display_img(self, *ims):
        if len(ims) == 1:
            self.im = ims[0]
        else:
            self.im = hstack(*ims)
