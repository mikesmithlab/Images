from __init__ import *
import cv2

__all__ = [
    "ThresholdGui",

]


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


class CircleGui(ParamGui):
    def __init__(self, img):
        self.grayscale = True
        self.param_dict = {
                    'distance': [25, 3, 51, 2],
                    'thresh1': [200, 0, 255, 1],
                    'thresh2': [5, 0, 20, 1],
                    'min_rad': [17, 3, 50, 1],
                    'max_rad': [19, 3, 50, 1]
                    }
        ParamGui.__init__(self, img)

    def update(self):
        circles = find_circles(self.im0, self.param_dict['distance'][0],
                               self.param_dict['thresh1'][0],
                               self.param_dict['thresh2'][0],
                               self.param_dict['min_rad'][0],
                               self.param_dict['max_rad'][0])
        self._display_img(draw_circles(gray_to_bgr(self.im0), circles))


class AdaptiveThresholdGui(ParamGui):

    def __init__(self, img, mode=cv2.THRESH_BINARY):
        self.grayscale = True
        self.param_dict = {'window': [3, 3, 101, 2],
                           'constant': [0, -30, 30, 1],
                           'invert': [0, 0, 1, 1]}
        self.mode = mode
        ParamGui.__init__(self, img)

    def update(self):
        if self.param_dict['invert'][0] == 0:
            self._display_img(adaptive_threshold(self.im0,
                                                 self.param_dict['window'][0],
                                                 self.param_dict['constant'][0],
                                                 mode=self.mode)
                              )
        else:
            self._display_img(adaptive_threshold(self.im0,
                                                 self.param_dict['window'][0],
                                                 self.param_dict['constant'][0],
                                                 mode=cv2.THRESH_BINARY_INV)
                              )


if __name__ == "__main__":
    from basics import load
    im = load("/home/ppxjd3/Pictures/hecx.png")
    pg = AdaptiveThresholdGui(im)