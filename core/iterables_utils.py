from itertools import chain, combinations, permutations
from timeit import default_timer
import sys
try:
    from . import memory
except Exception as e:
    import memory


def get_powerset(iterable):
    return chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1))


def get_permutations(iterable):
    return permutations(iterable)


if __name__ == '__main__':
    memory.memory_limit()
    try:
        time = default_timer()
        transformations = ['remove_mean', 'standardize', 'contrast_adjust', 'flip_lr', 'flip_ud', 'flip_lr_ud', 'image_pad', 'text_binarizarion', 'gaussian_blur', 'low_brightness_negative', 'edge_detection', 'enhance_basic_color', 'enhance_basic_contrast', 'enhance_basic_brightness', 'enhance_basic_sharpness', 'negative', 'intensity_increase', 'logarithmic_transformation', 'exponential_transformation', 'binarization', 'gray_fractionation', 'histogram_equalization', 'grayscale', 'posterize', 'solarize', 'remove_noise', 'clean_imagemagic', 'crop_morphology']

        print()
        print('---------------------------------------Permutations---------------------------------------')
        permutations_result = get_permutations(transformations)
        # for pipeline in permutations_result:
        #     print(pipeline)

        print()
        print('---------------------------------------Powerset---------------------------------------')
        powerset_result = get_powerset(transformations)
        # for pipeline in powerset_result:
        #     print(pipeline)

        time_end = default_timer() - time

        print()
        print('------------------------------------------------------------------------------------------')
        print("Total time execution: " + str(time_end))
    except MemoryError:
        sys.stderr.write('\n\nERROR: Memory Exception\n')
        sys.exit(1)
