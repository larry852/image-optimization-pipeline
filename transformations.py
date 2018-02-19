import math
import cv2
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
from extra import font_and_background_color_independent_text_binarization as text_binarizarion_lib
import os


def remove_mean(image):
    """
    remove RGB mean values which from ImageNet
    input:
        image:  RGB image np.ndarray
                type of elements is np.uint8
    return:
        image:  remove RGB mean and scale to [0,1]
                type of elements is np.float32
    """
    mean = [0.48462227599918, 0.45624044862054, 0.40588363755159]
    image = image.astype(np.float32)
    image = np.subtract(np.divide(image, 255.0), mean)
    return image


def standardize(image, mean=[0.48462227599918, 0.45624044862054, 0.40588363755159], std=[0.22889466674951, 0.22446679341259, 0.22495548344775]):
    """
    standardize RGB mean and std values which from ImageNet
    input:
        image:  RGB image np.ndarray
                type of elements is np.uint8
    return:
        image:  standarded image
                type of elements is np.float32
    """
    image = image.astype(np.float32) / 255.0
    image = np.divide(np.subtract(image, mean), std)
    return image


def contrast_adjust(image, alpha=1.3, beta=20):
    """
    adjust constrast through gamma correction
    newimg = image * alpha + beta
    input:
        image: np.uint8 or np.float32
    output:
        image: np.uint8 or np.float
    """
    newimage = image.astype(np.float32) * alpha + beta

    if type(image[0, 0, 0]) == np.uint8:
        newimage[newimage < 0] = 0
        newimage[newimage > 255] = 255
        return np.uint8(newimage)
    else:
        newimage[newimage < 0] = 0
        newimage[newimage > 1] = 1.
        return newimage


def flip(image, lr, ud):
    """
    flip image
    """
    if lr:
        image = cv2.flip(image, flipCode=1)
    if ud:
        image = cv2.flip(image, flipCode=0)
    return image


def image_crop(image, crop=None, random_crop=False):
    """
    if crop is None crop size is generated with a random size range from [0.5*height,height]
    if random_crop == True image croped from a random position
    input:
        image: image np.ndarray [H,W,C]
        crop: [target_height,target_width]
    output:
        croped image with shape[crop[0],crop[1],C]
    """
    hei, wid, _ = image.shape
    if crop is None:
        crop = (np.random.randint(int(hei / 2), hei),
                np.random.randint(int(wid / 2), wid))
    th, tw = [int(round(x / 2)) for x in crop]
    if random_crop:
        th, tw = np.random.randint(
            0, hei - crop[0] - 1), np.random.randint(0, wid - crop[1] - 1)
    return image[th:th + crop[0], tw:tw + crop[1]]


def image_pad(image, pad_width=None, axis=0, mode='symmetric'):
    """
    pad an image
    like np.pad way
    input:
        image: ndarray [rgb]

    """
    hei, wid = image.shape[0], image.shape[1]

    if pad_width is None:
        th = hei // 10
        tw = wid // 10
        pad_width = ((th, th), (tw, tw), (0, 0))
    if axis == 0:
        if type(pad_width[0]) == tuple:
            pad_width = (pad_width[0], (0, 0), (0, 0))
        else:
            pad_width = (pad_width, (0, 0), (0, 0))
    if axis == 1:
        if type(pad_width[0]) == tuple:
            pad_width = ((0, 0), pad_width[1], (0, 0))
        else:
            pad_width = ((0, 0), pad_width, (0, 0))
    if len(image.shape) == 3:
        newimage = np.pad(image, pad_width, mode)
    elif len(image.shape) == 2:
        newimage = np.squeeze(np.pad(image[:, :, np.newaxis], pad_width, mode))

    return cv2.resize(newimage, (wid, hei), interpolation=cv2.INTER_NEAREST)


def text_binarizarion(image):
    return text_binarizarion_lib.main(image)


def gaussian_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def otsu_thresholding(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[-1]


def low_brightness_negative(image, delta=-50):
    return image - delta


def edge_detection(image, sigma=0.33):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged


def enhance_basic_color(image):
    data = Image.fromarray(image)
    enhancer = ImageEnhance.Color(data)
    return np.asarray(enhancer.enhance(2))


def enhance_basic_contrast(image):
    data = Image.fromarray(image)
    enhancer = ImageEnhance.Contrast(data)
    return np.asarray(enhancer.enhance(2))


def enhance_basic_brightness(image):
    data = Image.fromarray(image)
    enhancer = ImageEnhance.Brightness(data)
    return np.asarray(enhancer.enhance(2))


def enhance_basic_sharpness(image):
    data = Image.fromarray(image)
    enhancer = ImageEnhance.Sharpness(data)
    return np.asarray(enhancer.enhance(4))


def negative(image):
    return 255 - image


def intensity_increase(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, columns = image.shape
    result = np.zeros((rows, columns), dtype=np.uint8)
    m = 0.8
    b = 100
    for x in range(0, rows):
        for y in range(0, columns):
            result[x, y] = m * image[x, y] + b
    return result


def logarithmic_transformation(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, columns = image.shape
    result = np.zeros((rows, columns), dtype=np.uint8)
    r = np.max(image)
    c = 255 / math.log10(1 + r)
    for x in range(0, rows):
        for y in range(0, columns):
            result[x, y] = c * math.log10(1 + image[x, y])
    return result


def exponential_transformation(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, columns = image.shape
    result = np.zeros((rows, columns), dtype=np.uint8)

    gamma = 0.08
    c = 255 / 255**gamma

    for x in range(0, rows):
        for y in range(0, columns):
            result[x, y] = c * image[x, y]**gamma
    return result


def binarization(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, columns = image.shape
    result = np.zeros((rows, columns), dtype=np.uint8)

    a = 50
    b = 100

    for x in range(0, rows):
        for y in range(0, columns):
            r = image[x][y]
            if a <= r and r <= b:
                result[x][y] = 255
            else:
                result[x][y] = 0
    return result


def gray_fractionation(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, columns = image.shape
    result = np.zeros((rows, columns), dtype=np.uint8)

    a = 50
    b = 200

    for x in range(0, rows):
        for y in range(0, columns):
            r = image[x][y]
            if a <= r and r <= b:
                result[x][y] = 255
            else:
                result[x][y] = image[x][y]
    return result


def histogram_equalization(image):
    image = Image.fromarray(image)
    return np.asarray(ImageOps.equalize(image))


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def posterize(image):
    image = Image.fromarray(image)
    return np.asarray(ImageOps.posterize(image, 1))


def solarize(image):
    image = Image.fromarray(image)
    return np.asarray(ImageOps.solarize(image, threshold=64))


def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


def clean_imagemagic(filepath, output='img/output/output-clean_imagemagic.png'):
    command = 'convert {} -morphology Convolve DoG:15,100,0 -negate -normalize -blur 0x1 -channel RBG -level 60%,91%,0.1 {}'.format(filepath, output)
    os.system(command)
