from PIL import Image
import numpy as np
import uuid
try:
    from . import transformations
except Exception:
    import transformations


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


def transformation(name, image):
    if name == 'remove_mean':
        return transformations.remove_mean(image)
    elif name == 'standardize':
        return transformations.standardize(image),
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
    elif name == 'text_binarizarion':
        return transformations.text_binarizarion(image)
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
    else:
        print('default')
        return image


def pipeline(filepath, steps):
    image = load_image(filepath)
    path_temp = 'static/img/temp/current.png'
    for step in steps:
        print(image)
        image = transformation(step, image)
        save_image(image, path_temp)
        image = load_image(path_temp)

    filename = '-'.join(steps) + '-' + str(uuid.uuid4()).split('-')[0]
    save_image(image, 'static/img/pipelines/{}.png'.format(filename))


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


if __name__ == '__main__':
    try:
        from . import iterables_utils
    except Exception:
        import iterables_utils

    # individual('/home/larry/image-optimization-pipeline/static/img/input/1.jpg')

    list_transformations = ['remove_mean', 'standardize', 'contrast_adjust', 'flip_lr', 'flip_ud', 'flip_lr_ud', 'image_pad', 'text_binarizarion', 'gaussian_blur', 'low_brightness_negative', 'edge_detection', 'enhance_basic_color', 'enhance_basic_contrast', 'enhance_basic_brightness', 'enhance_basic_sharpness', 'negative', 'intensity_increase', 'logarithmic_transformation', 'exponential_transformation', 'binarization', 'gray_fractionation', 'histogram_equalization', 'grayscale', 'posterize', 'solarize', 'remove_noise', 'clean_imagemagic', 'crop_morphology']
    permutations = iterables_utils.get_permutations(list_transformations)
    for steps in permutations:
        pipeline('/home/larry/image-optimization-pipeline/static/img/input/1.jpg', steps)
