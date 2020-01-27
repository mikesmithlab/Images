import tkinter as tk
import random
from PIL import Image, ImageTk


__all__ = [
    "ParamGui"
]


class ParamGui:

    def __init__(self, im):
        self.im = im
        self.width = im.shape[0]
        self.height = im.shape[1]
        self.param_dict = {'a': [3, 0, 10, .1], 'b': [0, -5, 5, 1]}
        self.init_ui()


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

        for key in sorted(self.param_dict.keys()):
            params = self.param_dict[key]
            val, bottom, top, step = params
            frame = tk.Frame(self.frame)
            label = tk.Label(frame, text=key)
            label.pack(side=tk.LEFT)
            var = tk.Variable(value=val)
            slider = tk.Scale(frame, from_=bottom, to=top, resolution=step, orient=tk.HORIZONTAL, length=self.im.shape[0]//2, command=self.slider_callback, variable=var)
            # slider.set(val)
            slider.pack(side=tk.LEFT, fill=tk.X)
            frame.pack()
            self.sliders[key] = slider

    def _update_sliders(self):
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

from basics import load
im = load("/home/ppxjd3/Pictures/hecx.png")
pg = ParamGui(im)