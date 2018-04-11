from PIL import Image
import numpy as np
from . import transformations
import uuid


def load_image(filepath):
    img = Image.open(filepath)
    img.load()
    data = np.asarray(img)
    return data


def save_image(npdata, outfilename):
    try:
        if not type(npdata[0, 0, 0]) == np.uint8:
            npdata = (npdata * 255).round().astype(np.uint8)
    except Exception:
        pass
    img = Image.fromarray(npdata)
    img.save(outfilename)


def transformation(name, original, filepath):
    return {
        'remove_mean': transformations.remove_mean(original),
        'standardize': transformations.standardize(original),
        'contrast_adjust': transformations.contrast_adjust(original),
        'flip_lr': transformations.flip(original, True, False),
        'flip_ud': transformations.flip(original, False, True),
        'flip_lr_ud': transformations.flip(original, True, True),
        'image_pad': transformations.image_pad(original),
        'text_binarizarion': transformations.text_binarizarion(original),
        'gaussian_blur': transformations.gaussian_blur(original),
        'low_brightness_negative': transformations.low_brightness_negative(original),
        'edge_detection': transformations.edge_detection(original),
        'enhance_basic_color': transformations.enhance_basic_color(original),
        'enhance_basic_contrast': transformations.enhance_basic_contrast(original),
        'enhance_basic_brightness': transformations.enhance_basic_brightness(original),
        'enhance_basic_sharpness': transformations.enhance_basic_sharpness(original),
        'negative': transformations.negative(original),
        'intensity_increase': transformations.intensity_increase(original),
        'logarithmic_transformation': transformations.logarithmic_transformation(original),
        'exponential_transformation': transformations.exponential_transformation(original),
        'binarization': transformations.binarization(original),
        'gray_fractionation': transformations.gray_fractionation(original),
        'histogram_equalization': transformations.histogram_equalization(original),
        'grayscale': transformations.grayscale(original),
        'posterize': transformations.posterize(original),
        'solarize': transformations.solarize(original),
        'remove_noise': transformations.remove_noise(original),
        'clean_imagemagic': transformations.clean_imagemagic(filepath),
        'crop_morphology': transformations.crop_morphology(original),
    }.get(name, original)


def individual(filepath):
    original = load_image(filepath)
    results = []
    result = {'transformation': 'remove_mean', 'image': transformations.remove_mean(original)}
    results.append(result)
    result = {'transformation': 'standardize', 'image': transformations.standardize(original)}
    results.append(result)
    result = {'transformation': 'contrast_adjust', 'image': transformations.contrast_adjust(original)}
    results.append(result)
    result = {'transformation': 'flip_lr', 'image': transformations.flip(original, True, False)}
    results.append(result)
    result = {'transformation': 'flip_ud', 'image': transformations.flip(original, False, True)}
    results.append(result)
    result = {'transformation': 'flip_lr_ud', 'image': transformations.flip(original, True, True)}
    results.append(result)
    result = {'transformation': 'image_pad', 'image': transformations.image_pad(original)}
    results.append(result)
    result = {'transformation': 'text_binarizarion', 'image': transformations.text_binarizarion(original)}
    results.append(result)
    result = {'transformation': 'gaussian_blur', 'image': transformations.gaussian_blur(original)}
    results.append(result)
    result = {'transformation': 'low_brightness_negative', 'image': transformations.low_brightness_negative(original)}
    results.append(result)
    result = {'transformation': 'edge_detection', 'image': transformations.edge_detection(original)}
    results.append(result)
    result = {'transformation': 'enhance_basic_color', 'image': transformations.enhance_basic_color(original)}
    results.append(result)
    result = {'transformation': 'enhance_basic_contrast', 'image': transformations.enhance_basic_contrast(original)}
    results.append(result)
    result = {'transformation': 'enhance_basic_brightness', 'image': transformations.enhance_basic_brightness(original)}
    results.append(result)
    result = {'transformation': 'enhance_basic_sharpness', 'image': transformations.enhance_basic_sharpness(original)}
    results.append(result)
    result = {'transformation': 'negative', 'image': transformations.negative(original)}
    results.append(result)
    result = {'transformation': 'intensity_increase', 'image': transformations.intensity_increase(original)}
    results.append(result)
    result = {'transformation': 'logarithmic_transformation', 'image': transformations.logarithmic_transformation(original)}
    results.append(result)
    result = {'transformation': 'exponential_transformation', 'image': transformations.exponential_transformation(original)}
    results.append(result)
    result = {'transformation': 'binarization', 'image': transformations.binarization(original)}
    results.append(result)
    result = {'transformation': 'gray_fractionation', 'image': transformations.gray_fractionation(original)}
    results.append(result)
    result = {'transformation': 'histogram_equalization', 'image': transformations.histogram_equalization(original)}
    results.append(result)
    result = {'transformation': 'grayscale', 'image': transformations.grayscale(original)}
    results.append(result)
    result = {'transformation': 'posterize', 'image': transformations.posterize(original)}
    results.append(result)
    result = {'transformation': 'solarize', 'image': transformations.solarize(original)}
    results.append(result)
    result = {'transformation': 'remove_noise', 'image': transformations.remove_noise(original)}
    results.append(result)
    result = {'transformation': 'clean_imagemagic', 'image': transformations.clean_imagemagic(filepath)}
    results.append(result)
    result = {'transformation': 'crop_morphology', 'image': transformations.crop_morphology(original)}
    results.append(result)
    for result in results:
        if result['image'] is not None:
            filename = result['transformation'] + '-' + str(uuid.uuid4()).split('-')[0]
            save_image(result['image'], 'static/img/output/{}.png'.format(filename))
