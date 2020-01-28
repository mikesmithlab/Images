from __init__ import *
import cv2

class ThresholdGui(ParamGui):
    def __init__(self, im):
        self.grayscale = True
        self.param_dict = {
            'threshold': [1, 0, 255, 1],
            'invert': [0, 0, 1, 1]}
        ParamGui.__init__(self, im)

    def update(self):
        if self.param_dict['invert'][0] == 0:
            self._display_img(threshold(self.im0,
                                value=self.param_dict['threshold'][0]))
        else:
            self._display_img(threshold(self.im0,
                                value=self.param_dict['threshold'][0],
                                mode=cv2.THRESH_BINARY_INV))


if __name__ == "__main__":
    from basics import load
    im = load("/home/ppxjd3/Pictures/hecx.png")
    pg = ThresholdGui(im)