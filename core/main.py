from PIL import Image
import numpy as np
import uuid
from os import makedirs, path
from shutil import rmtree
import logging
try:
    from . import transformations
    from . import iterables_utils
except Exception:
    import transformations
    import iterables_utils

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(message)s')


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


def transformation(name, filepath):
    image = load_image(filepath)
    if name == 'remove_mean':
        return transformations.remove_mean(image)
    elif name == 'standardize':
        return transformations.standardize(image)
    elif name == 'contrast_adjust':
        return transformations.contrast_adjust(image)
    elif name == 'flip_lr':
        return transformations.flip(image, True, False)
    elif name == 'flip_ud':
        return transformations.flip(image, False, True)
    elif name == 'flip_lr_ud':
        return transformations.flip(image, True, True)
    elif name == 'image_pad':
        return transformations.image_pad(image)
    elif name == 'text_binarization':
        return transformations.text_binarization(image)
    elif name == 'gaussian_blur':
        return transformations.gaussian_blur(image)
    elif name == 'low_brightness_negative':
        return transformations.low_brightness_negative(image)
    elif name == 'edge_detection':
        return transformations.edge_detection(image)
    elif name == 'enhance_basic_color':
        return transformations.enhance_basic_color(image)
    elif name == 'enhance_basic_contrast':
        return transformations.enhance_basic_contrast(image)
    elif name == 'enhance_basic_brightness':
        return transformations.enhance_basic_brightness(image)
    elif name == 'enhance_basic_sharpness':
        return transformations.enhance_basic_sharpness(image)
    elif name == 'negative':
        return transformations.negative(image)
    elif name == 'intensity_increase':
        return transformations.intensity_increase(image)
    elif name == 'logarithmic_transformation':
        return transformations.logarithmic_transformation(image)
    elif name == 'exponential_transformation':
        return transformations.exponential_transformation(image)
    elif name == 'binarization':
        return transformations.binarization(image)
    elif name == 'gray_fractionation':
        return transformations.gray_fractionation(image)
    elif name == 'histogram_equalization':
        return transformations.histogram_equalization(image)
    elif name == 'grayscale':
        return transformations.grayscale(image)
    elif name == 'posterize':
        return transformations.posterize(image)
    elif name == 'solarize':
        return transformations.solarize(image)
    elif name == 'remove_noise':
        return transformations.remove_noise(image)
    elif name == 'crop_morphology':
        return transformations.crop_morphology(image)
    elif name == 'clean_imagemagic':
        return transformations.clean_imagemagic(filepath)
    else:
        return image


def run_pipeline(filepath, steps, folder=0):
    path_temp = 'static/img/pipelines/steps/{}/{}.png'
    for index, step in enumerate(steps):
        try:
            image = transformation(step, filepath)
        except Exception:
            logging.debug('[FAIL] Pipeline {}. Steps {} - Step {}'.format(folder, steps, step))
            return None
        filename = str(index + 1) + ')' + step + '-' + str(uuid.uuid4()).split('-')[0]
        filepath = path_temp.format(folder, filename)
        save_image(image, filepath)
    return image


def pipeline(filepath, list_transformations):
    permutations = iterables_utils.get_permutations(list_transformations)
    steps_directory = 'static/img/pipelines/steps/'
    if not path.exists(steps_directory):
        makedirs(steps_directory)
    else:
        rmtree(steps_directory)
        makedirs(steps_directory)
    for index, steps in enumerate(permutations):
        folder = index + 1
        makedirs('static/img/pipelines/steps/{}'.format(folder))
        image = run_pipeline(filepath, steps, folder)
        if image is not None:
            logging.debug('[SUCCESS] Pipeline {}. Steps {}'.format(folder, steps))
            filename = str(folder) + '-' + str(uuid.uuid4()).split('-')[0]
            save_image(image, 'static/img/pipelines/results/{}.png'.format(filename))


def pipeline_individual(filepath, steps):
    steps_directory = 'static/img/pipelines/steps/'
    if not path.exists(steps_directory):
        makedirs(steps_directory)
    else:
        rmtree(steps_directory)
        makedirs(steps_directory)

    folder = 1
    makedirs('static/img/pipelines/steps/{}'.format(folder))
    image = run_pipeline(filepath, steps, folder)
    if image is not None:
        logging.debug('[SUCCESS] Pipeline {}. Steps {}'.format(folder, steps))
        filename = str(folder) + '-' + str(uuid.uuid4()).split('-')[0]
        save_image(image, 'static/img/pipelines/results/{}.png'.format(filename))


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
    result = {'transformation': 'text_binarization', 'image': transformations.text_binarization(original)}
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
    result = {'transformation': 'crop_morphology', 'image': transformations.crop_morphology(original)}
    results.append(result)
    result = {'transformation': 'clean_imagemagic', 'image': transformations.clean_imagemagic(filepath)}
    results.append(result)
    for result in results:
        filename = result['transformation'] + '-' + str(uuid.uuid4()).split('-')[0]
        save_image(result['image'], 'static/img/output/{}.png'.format(filename))
