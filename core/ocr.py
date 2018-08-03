from PIL import Image
import pytesseract
from fuzzywuzzy import fuzz


def compare(text, path):
    result = Image.open(path)
    result_text = pytesseract.image_to_string(result, lang='spa')
    return result_text, fuzz.token_set_ratio(text, result_text)


def extract(path):
    result = Image.open(path)
    result_text = pytesseract.image_to_string(result, lang='spa')
    return result_text
