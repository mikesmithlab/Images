from cropping import crop_circle, crop_and_mask
from basics import load, plot

im = load("/home/ppxjd3/Pictures/hecx.png")
ic = crop_circle(im)
print(im.shape)
print(ic.mask.shape)
im = crop_and_mask(im, ic.bbox, ic.mask)
plot(im)
print(ic)