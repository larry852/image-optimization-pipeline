from core import main as processing_lib
from core import ocr
import utils
from operator import itemgetter
from static.img.original_texts import ORIGINAL_TEXTS


config = {}
config['INPUT_FOLDER'] = 'static/img/input/'
config['OUTPUT_FOLDER'] = 'static/img/output/'
config['OUTPUT_FOLDER_PIPELINES'] = 'static/img/pipelines/results'
config['OUTPUT_FOLDER_STEPS'] = 'static/img/pipelines/steps'
config['TRANSFORMATIONS'] = ['solarize', 'posterize', 'enhance_basic_sharpness', 'crop_morphology', 'clean_imagemagic', ]
config['TRANSFORMATIONS'] = ['crop_morphology', ]


def main():
    utils.delete_images(config['OUTPUT_FOLDER_PIPELINES'])
    images = utils.get_images(config['INPUT_FOLDER'])
    for image in images:
        filepath = image[0][1:]
        text = ORIGINAL_TEXTS[image[1]]

        processing_lib.pipeline(filepath, config['TRANSFORMATIONS'])

        pipelines = utils.get_images(config['OUTPUT_FOLDER_PIPELINES'])
        pipelines.sort(key=lambda x: int(x[1].split('-')[0]))
        results = []
        for pipeline in pipelines:
            result_text, percentage = ocr.compare(text, utils.get_filepath(config['OUTPUT_FOLDER_PIPELINES'], pipeline[1]))
            results.append({'pipeline': pipeline[1].split('-')[0], 'original': text, 'result': result_text, 'percentage': percentage})

        results = sorted(results, key=itemgetter('percentage'), reverse=True)

        result_text, percentage = ocr.compare(text, filepath)
        results.insert(0, {'pipeline': 'original', 'original': text, 'result': result_text, 'percentage': percentage})

        print(results)

        break


if __name__ == '__main__':
    main()
