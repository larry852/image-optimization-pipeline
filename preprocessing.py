from PIL import Image
import numpy as np
import transformations


def load_image(filename):
    img = Image.open(filename)
    img.load()
    data = np.asarray(img)
    return data


def save_image(npdata, outfilename):
    if not type(npdata[0, 0, 0]) == np.uint8:
        npdata = (npdata * 255).round().astype(np.uint8)
    img = Image.fromarray(npdata)
    img.save(outfilename)


if __name__ == "__main__":
    original = load_image('img/input/04.jpg')
    results = []
    result = {'transformation': 'remove_mean', 'image': transformations.remove_mean(original)}
    results.append(result)
    result = {'transformation': 'standardize', 'image': transformations.standardize(original)}
    results.append(result)
    result = {'transformation': 'samele_wise_normalization', 'image': transformations.samele_wise_normalization(original)}
    results.append(result)
    result = {'transformation': 'contrast_adjust', 'image': transformations.contrast_adjust(original)}
    results.append(result)
    for result in results:
        save_image(result['image'], 'img/output/output-{}.png'.format(result['transformation']))
