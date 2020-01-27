from __init__ import *
import numpy as np

def test_draw_circle():
    im = load("/home/ppxjd3/Pictures/hecx.png")
    im = draw_circle(im, 40, 50, 10)
    plot(im)

def test_draw_circles():
    im = load("/home/ppxjd3/Pictures/hecx.png")
    circles = np.array([[10, 10, 5], [50, 50, 15]])
    im = draw_circles(im, circles)
    plot(im)

def test_draw_circles_with_scale():
    im = load("/home/ppxjd3/Pictures/hecx.png")
    circles = np.array([[10, 10, 5], [50, 50, 15]])
    values = [10, 100]
    im = draw_circles_with_scale(im, circles, values)
    plot(im)


test_draw_circle()
test_draw_circles()
test_draw_circles_with_scale()