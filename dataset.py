from core import main as processing_lib
from core import ocr
import utils
from static.img.original_texts import ORIGINAL_TEXTS
import csv
from timeit import default_timer


config = {}
config['INPUT_FOLDER'] = 'static/img/input/'
config['OUTPUT_FOLDER'] = 'static/img/output/'
config['OUTPUT_FOLDER_PIPELINES'] = 'static/img/pipelines/results'
config['OUTPUT_FOLDER_STEPS'] = 'static/img/pipelines/steps/'
config['TRANSFORMATIONS'] = ['solarize', 'posterize', 'enhance_basic_sharpness', 'crop_morphology', 'clean_imagemagic', ]


def main(image=0):
    if image == 0:
        init__file_results()

    images = utils.get_images(config['INPUT_FOLDER'])
    images.sort(key=lambda x: int(x[1]))
    images = images[image:]

    for image in images:
        print('Image {}'.format(image[1]))
        filepath = image[0][1:]
        text = ORIGINAL_TEXTS[image[1]]
        utils.delete_images(config['OUTPUT_FOLDER_PIPELINES'])

        time = default_timer()
        result_text, percentage = ocr.compare(text, filepath)
        time_end = default_timer() - time
        write__file_result([image[1], 'original', percentage, text, result_text, time_end])

        steps, times = processing_lib.pipeline(filepath, config['TRANSFORMATIONS'])

        pipelines = utils.get_images(config['OUTPUT_FOLDER_PIPELINES'])
        for pipeline in pipelines:
            time = default_timer()
            result_text, percentage = ocr.compare(text, utils.get_filepath(config['OUTPUT_FOLDER_PIPELINES'], pipeline[1]))
            time_end = default_timer() - time
            write__file_result([image[1], '\r'.join(steps[int(pipeline[1].split('-')[0])]), percentage, text, result_text, times[int(pipeline[1].split('-')[0])] + time_end])


def write__file_result(row):
    with open('results.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()


def init__file_results():
    with open('results.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['IMAGEN', 'PIPELINE', 'PORCENTAJE DE SIMILITUD', 'TEXTO ORIGINAL', 'TEXTO DETECTADO', 'TIEMPO(PIPELINE INDIVIDUAL + OCR + VALIDACION)'])
    csvFile.close()


if __name__ == '__main__':
    time = default_timer()
    main()
    time_end = default_timer() - time
    print('Total time execution: {}'.format(time_end))
    write__file_result(['', '', '', '', 'TIEMPO TOTAL (FOREST + PIPELINES + OCRS + VALIDACIONES)', time_end])
