from core import main as processing_lib
import utils


config = {}
config['INPUT_FOLDER'] = 'static/img/input/'
config['OUTPUT_FOLDER'] = 'static/img/output/'
config['OUTPUT_FOLDER_PIPELINES'] = 'static/img/pipelines/results'
config['OUTPUT_FOLDER_STEPS'] = 'static/img/pipelines/steps'
config['TRANSFORMATIONS'] = ['solarize', 'posterize', 'enhance_basic_sharpness', 'crop_morphology', 'clean_imagemagic', ]
config['TRANSFORMATIONS'] = ['solarize', 'posterize', ]


def main():
    utils.delete_images(config['OUTPUT_FOLDER_PIPELINES'])
    images = utils.get_images(config['INPUT_FOLDER'])
    for image in images:
        processing_lib.pipeline(image[0][1:], config['TRANSFORMATIONS'])
        break


if __name__ == '__main__':
    main()
