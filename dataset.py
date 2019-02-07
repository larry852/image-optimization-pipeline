from core import main as processing_lib
from core import ocr
import utils
from operator import itemgetter
from static.img.original_texts import ORIGINAL_TEXTS
import csv


config = {}
config['INPUT_FOLDER'] = 'static/img/input/'
config['OUTPUT_FOLDER'] = 'static/img/output/'
config['OUTPUT_FOLDER_PIPELINES'] = 'static/img/pipelines/results'
config['OUTPUT_FOLDER_STEPS'] = 'static/img/pipelines/steps/'
config['TRANSFORMATIONS'] = ['solarize', 'posterize', 'enhance_basic_sharpness', 'crop_morphology', 'clean_imagemagic', ]
config['TRANSFORMATIONS'] = ['crop_morphology', 'enhance_basic_sharpness', ]


def main():
    init_results()
    utils.delete_images(config['OUTPUT_FOLDER_PIPELINES'])
    images = utils.get_images(config['INPUT_FOLDER'])
    for image in images:
        filepath = image[0][1:]
        text = ORIGINAL_TEXTS[image[1]]

        result_text, percentage = ocr.compare(text, filepath)
        write_result([image[1], 'original', text, result_text, percentage])

        processing_lib.pipeline(filepath, config['TRANSFORMATIONS'])

        pipelines = utils.get_images(config['OUTPUT_FOLDER_PIPELINES'])
        pipelines.sort(key=lambda x: int(x[1].split('-')[0]))
        for pipeline in pipelines:
            result_text, percentage = ocr.compare(text, utils.get_filepath(config['OUTPUT_FOLDER_PIPELINES'], pipeline[1]))
            steps = utils.get_images(config['OUTPUT_FOLDER_STEPS'] + pipeline[1].split('-')[0])
            steps.sort(key=lambda x: int(x[1].split(')')[0]))
            steps = [step[1].split('-')[0] for step in steps]

            write_result([image[1], ' '.join(steps), text, result_text, percentage])
        break


def write_result(row):
    with open('results.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()


def init_results():
    with open('results.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['imagen', 'pipeline', 'texto original', 'texto detectado', 'porcentaje'])
    csvFile.close()


if __name__ == '__main__':
    main()
