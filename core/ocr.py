from PIL import Image
import pytesseract
from fuzzywuzzy import fuzz


def compare(original_path, result_path):
    result = Image.open(result_path)
    original_text = 'LUIS ALEJANDRO ALENCASTRO CIFUENTES'
    result_text = pytesseract.image_to_string(result, lang='spa')
    return original_text, result_text, fuzz.token_set_ratio(original_text, result_text)


if __name__ == '__main__':
    print(compare('/home/larry/image-optimization-pipeline/static/img/input/2.jpg', '/home/larry/image-optimization-pipeline/static/img/pipelines/results/1-ccc3dcab.png'))
