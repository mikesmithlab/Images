from cropping import crop_polygon
from basics import load

im = load("/home/ppxjd3/Pictures/hecx.png")
ic = crop_polygon(im)
print(ic)