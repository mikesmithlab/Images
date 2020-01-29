import cv2
import matplotlib.pyplot as plt
import numpy as np

__all__ = [
    'display',
    'plot',
    'read_img',
    'load',
    'read',
    'write_img',
    'save',
    'write',
    'width_and_height',
    'dimensions',
    'height',
    'width',
    'to_uint8',
    'Displayer',
    'mean',
    'depth'
]


class Displayer:
    def __init__(self, window_name, resolution=(1280, 720)):
        self.window_name = window_name
        cv2.namedWindow(self.window_name, cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(self.window_name, *resolution)

    def update_im(self, im):
        cv2.imshow(self.window_name, im)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            pass


def mean(ims):
    im = np.stack(ims, axis=len(np.shape(ims[0])))
    im = np.float32(im)
    im = np.mean(im, axis=len(np.shape(ims[0])))
    return np.uint8(im)

def display(image, title='', resolution=(960, 540)):
    """Uses cv2 to display an image then wait for a button press"""
    cv2.namedWindow(title, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(title, *resolution)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def plot(im):
    plt.figure()
    plt.imshow(im)
    plt.show()

def to_uint8(im):
    im = (im - np.min(im))/(np.max(im)-np.min(im)) * 255
    return np.uint8(im)

def read_img(filepath, flag=1):
    """
    Reads an image from a filepath.

    The image should be in the working directory or a full path of image
    should be given.

    Parameters
    ----------
    filepath: filepath of the image

    flag: Specifies how the image is read
        1: Loads a color image. Any transparency will be neglected.
        0: Loads image in grayscale mode.
        -1: Loads image including alpha channel

    Returns
    -------
    img: output image
        Number of channels will be determined by the chosen flag.
        Equal to None if filepath does not exist
        Color images will have channels stored in BGR order

    """
    img = cv2.imread(filepath, flag)
    return img


load = read_img
read = read_img


def write_img(img, filename):
    """
    Saves an image to a specified file.

    The image format is chosen based on the filename extension

    Parameters
    ----------
    img: Image to be saved

    filename: Name of the file

    Notes
    -----
    Only 8-bit single channel or 3-channel (BGR order) can be saved. If
    the format, depth or channel order is different convert it first.

    It is possible to store PNG images with an alpha channel using this
    function. To do this, create 8-bit 4-channel image BGRA, where the alpha
    channel goes last. Fully transparent pixels should have alpha set to 0,
    fully opaque pixels should have alpha set to 255

    """
    cv2.imwrite(filename, img)


save = write_img
write = write_img


def width_and_height(img):
    """
    Returns width, height for an image

    Parameters
    ----------
    img: Array containing an image

    Returns
    -------
    width: int
        Width of the image
    height: int
        Height of the image

    Notes
    -----
    Width of an image is the first dimension for numpy arrays.
    Height of an image is the first dimension for openCV
    """
    w = width(img)
    h = height(img)
    return w, h


dimensions = width_and_height


def width(img):
    """
    Returns width for img

    Parameters
    ----------
    img: Array containing an image

    Returns
    -------
    width: int
        Width of the image

    """
    return int(np.shape(img)[1])


def height(img):
    """
    Returns the height of an image

    Parameters
    ----------
    img: Array containing an image

    Returns
    -------
    height: int
        height of the image

    """
    return int(np.shape(img)[0])


def depth(img):
    shp = np.shape(img)
    if len(shp) == 2:
        return 1
    else:
        return shp[2]
