from itertools import chain, combinations, permutations
from timeit import default_timer


def powerset_list(iterable):
    return list(chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1)))


def permutations_list(iterable):
    return list(permutations(iterable))


if __name__ == '__main__':
    time = default_timer()
    # transformations = ['remove_mean', 'standardize', 'contrast_adjust', 'flip_lr', 'flip_ud', 'flip_lr_ud', 'image_pad', 'text_binarizarion', 'gaussian_blur', 'low_brightness_negative', 'edge_detection', 'enhance_basic_color', 'enhance_basic_contrast', 'enhance_basic_brightness', 'enhance_basic_sharpness', 'negative', 'intensity_increase', 'logarithmic_transformation', 'exponential_transformation', 'binarization', 'gray_fractionation', 'histogram_equalization', 'grayscale', 'posterize', 'solarize', 'remove_noise', 'clean_imagemagic', 'crop_morphology']
    transformations = ['histogram_equalization', 'grayscale', 'posterize', 'solarize', 'remove_noise', 'clean_imagemagic', 'crop_morphology', 'remove_mean', 'gaussian_blur', 'contrast_adjust']

    print()
    print('---------------------------------------Permutations---------------------------------------')
    permutations_result = permutations_list(transformations)
    # for pipeline in permutations_result:
    #     print(pipeline)

    print()
    print('---------------------------------------Powerset---------------------------------------')
    powerset_result = powerset_list(transformations)
    # for pipeline in powerset_result:
    #     print(pipeline)

    time_end = default_timer() - time

    print()
    print('------------------------------------------------------------------------------------------')
    print("Total powerset:" + str(len(powerset_result)))
    print("Total permutations:" + str(len(permutations_result)))
    print("Total time execution: " + str(time_end))
