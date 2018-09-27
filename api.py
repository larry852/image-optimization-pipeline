from flask import Flask, request, jsonify, redirect
from os.path import join
from core import main as processing_lib
from core import ocr
import utils
import uuid
from operator import itemgetter
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['INPUT_FOLDER'] = 'static/img/input/'
app.config['OUTPUT_FOLDER'] = 'static/img/output/'
app.config['OUTPUT_FOLDER_PIPELINES'] = 'static/img/pipelines/results'
app.config['OUTPUT_FOLDER_STEPS'] = 'static/img/pipelines/steps'


@app.route('/', methods=['GET'])
def api_root():
    return 'image-optimization-pipeline Aplicación de múltiples técnicas y transformación en imágenes para su optimización.'


@app.route('/upload', methods=['POST'])
def upload():
    images = utils.get_images(app.config['INPUT_FOLDER'])
    images.sort(key=lambda x: int(x[1]), reverse=True)
    new_file = request.files.get('img', None)
    if new_file is not None and utils.is_allowed_file(new_file.filename):
        filename = str(len(images) + 1) + '.' + new_file.filename.rsplit('.', 1)[1].lower()
        new_file.save(join(app.config['INPUT_FOLDER'], filename))
        response = jsonify({'success': True, 'id': filename.split('.')[0]})
        response.status_code = 200
        return response
    response = jsonify({'success': False, 'message': 'Invalid image file'})
    response.status_code = 400
    return response


@app.route('/processing/<image>', methods=['GET'])
def processing(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return not_found_error()
    utils.delete_images(app.config['OUTPUT_FOLDER'])
    processing_lib.individual(filepath)
    original = ['/' + filepath, image]
    transformations = utils.get_images(app.config['OUTPUT_FOLDER'])
    transformations.sort(key=lambda x: x[1])
    response = jsonify({'success': True, 'original': original, 'transformations': transformations})
    response.status_code = 200
    return response


@app.route('/pipelines/<image>', methods=['POST'])
def get_pipelines(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return not_found_error()
    utils.delete_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    list_transformations = request.get_json().get('list_transformations')
    if list_transformations is None:
        response = jsonify({'success': False, 'message': 'Field "list_transformations" is required'})
        response.status_code = 404
        return response
    processing_lib.pipeline(filepath, list_transformations)
    original = ['/' + filepath, image]
    pipelines = utils.get_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    steps_count = utils.count_folders(app.config['OUTPUT_FOLDER_STEPS'])
    for index in range(1, steps_count + 1):
        if next((x for x in pipelines if int(x[1].split('-')[0]) == index), None) is None:
            pipelines.append(('/static/img/fail.gif', '{}-{}'.format(index, str(uuid.uuid4()).split('-')[0])))
    pipelines.sort(key=lambda x: int(x[1].split('-')[0]))
    response = jsonify({'success': True, 'original': original, 'pipelines': pipelines})
    response.status_code = 200
    return response


@app.route('/pipeline/<image>', methods=['POST'])
def get_pipeline(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return not_found_error()
    utils.delete_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    steps = request.get_json().get('steps')
    if steps is None:
        response = jsonify({'success': False, 'message': 'Field "steps" is required'})
        response.status_code = 404
        return response
    processing_lib.pipeline_individual(filepath, steps)
    original = ['/' + filepath, image]
    pipelines = utils.get_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    steps_count = utils.count_folders(app.config['OUTPUT_FOLDER_STEPS'])
    for index in range(1, steps_count + 1):
        if next((x for x in pipelines if int(x[1].split('-')[0]) == index), None) is None:
            pipelines.append(('/static/img/fail.gif', '{}-{}'.format(index, str(uuid.uuid4()).split('-')[0])))
    pipelines.sort(key=lambda x: int(x[1].split('-')[0]))
    response = jsonify({'success': True, 'original': original, 'pipeline': pipelines})
    response.status_code = 200
    return response


@app.route('/ocr/<image>', methods=['POST'])
def get_ocr(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return not_found_error()
    text = request.get_json().get('text')
    if text is None:
        response = jsonify({'success': False, 'message': 'Field "text" is required'})
        response.status_code = 400
        return response
    pipelines = utils.get_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    pipelines.sort(key=lambda x: int(x[1].split('-')[0]))
    results = []
    for pipeline in pipelines:
        result_text, percentage = ocr.compare(text, utils.get_filepath(app.config['OUTPUT_FOLDER_PIPELINES'], pipeline[1]))
        results.append({'pipeline': pipeline[1].split('-')[0], 'original': text, 'result': result_text, 'percentage': percentage})
    results = sorted(results, key=itemgetter('percentage'), reverse=True)

    result_text, percentage = ocr.compare(text, filepath)
    results.insert(0, {'pipeline': 'original', 'original': text, 'result': result_text, 'percentage': percentage})
    response = jsonify({'success': True, 'results': results})
    response.status_code = 200
    return response


@app.route('/steps/<pipeline>/', methods=['GET'])
def steps(pipeline):
    pipeline = int(pipeline.split('-')[0])
    steps = utils.get_images('static/img/pipelines/steps/{}'.format(pipeline))
    steps.sort(key=lambda x: int(x[1].split(')')[0]))
    response = jsonify({'success': True, 'steps': steps, 'pipeline': pipeline})
    response.status_code = 200
    return response


@app.route('/ocr-steps/<original>/<folder>', methods=['POST'])
def get_ocr_steps(original, folder):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], original)
    if filepath is None:
        return not_found_error()
    text = request.get_json().get('text')
    if text is None:
        response = jsonify({'success': False, 'message': 'Field "text" is required'})
        response.status_code = 400
        return response
    steps = utils.get_images('static/img/pipelines/steps/{}'.format(folder))
    steps.sort(key=lambda x: int(x[1].split(')')[0]))
    results = []
    for step in steps:
        result_text, percentage = ocr.compare(text, utils.get_filepath('static/img/pipelines/steps/{}'.format(folder), step[1]))
        results.append({'step': step[1].split('-')[0], 'original': text, 'result': result_text, 'percentage': percentage})

    result_text, percentage = ocr.compare(text, filepath)
    results.insert(0, {'step': 'original', 'original': text, 'result': result_text, 'percentage': percentage})
    response = jsonify({'success': True, 'results': results})
    response.status_code = 200
    return response


@app.route('/ocr-individual/<pipeline>', methods=['GET'])
def get_ocr_inidividual(pipeline):
    filepath = utils.get_filepath(app.config['OUTPUT_FOLDER_PIPELINES'], pipeline)
    if filepath is None:
        return not_found_error()
    text = ocr.extract(filepath)
    results = {'pipeline': pipeline, 'text': text}
    response = jsonify({'success': True, 'results': results})
    response.status_code = 200
    return response


def not_found_error():
    response = jsonify({'success': False, 'message': 'Image not found'})
    response.status_code = 404
    return response


@app.before_request
def force_https():
    if not request.is_secure:
        print("http")
        return redirect(request.url.replace('http://', 'https://'))


if __name__ == "__main__":
    context = ('/etc/letsencrypt/live/loencontre.co/fullchain.pem', '/etc/letsencrypt/live/loencontre.co/privkey.pem')
    app.run(host='0.0.0.0', debug=False, port=8000, ssl_context=context)
