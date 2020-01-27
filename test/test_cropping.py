from cropping import crop_circle
from basics import load

im = load("/home/ppxjd3/Pictures/hecx.png")
ic = crop_circle(im)
print(ic)