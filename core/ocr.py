from PIL import Image
import pytesseract
from fuzzywuzzy import fuzz


def compare(text, path):
    result = Image.open(path)
    result_text = pytesseract.image_to_string(result, lang='spa')
    return result_text, fuzz.token_set_ratio(text, result_text)


if __name__ == '__main__':
    print(compare('LUIS ALEJANDRO ALENCASTRO CIFUENTES', '/home/larry/image-optimization-pipeline/static/img/pipelines/results/1-ccc3dcab.png'))
