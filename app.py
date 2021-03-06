from flask import Flask, render_template, request, url_for, redirect, jsonify
from os.path import join
from core import main as processing_lib
from core import ocr
import utils
import uuid
from operator import itemgetter


app = Flask(__name__)
app.config['INPUT_FOLDER'] = 'static/img/input/'
app.config['OUTPUT_FOLDER'] = 'static/img/output/'
app.config['OUTPUT_FOLDER_PIPELINES'] = 'static/img/pipelines/results'
app.config['OUTPUT_FOLDER_STEPS'] = 'static/img/pipelines/steps'


@app.route('/', methods=['GET', 'POST'])
def index():
    images = utils.get_images(app.config['INPUT_FOLDER'])
    images.sort(key=lambda x: int(x[1]), reverse=True)
    if request.method == 'POST':
        new_file = request.files.get('file', None)
        if new_file is not None and utils.is_allowed_file(new_file.filename):
            filename = str(len(images) + 1) + '.' + new_file.filename.rsplit('.', 1)[1].lower()
            new_file.save(join(app.config['INPUT_FOLDER'], filename))
            return redirect(url_for('processing', image=filename.split('.')[0]))
    return render_template('index.html', images=images)


@app.route('/processing/<image>')
def processing(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return redirect(url_for('index'))
    utils.delete_images(app.config['OUTPUT_FOLDER'])
    processing_lib.individual(filepath)
    original = ['/' + filepath, image]
    transformations = utils.get_images(app.config['OUTPUT_FOLDER'])
    transformations.sort(key=lambda x: x[1])
    return render_template('processing.html', original=original, transformations=transformations)


@app.route('/pipeline/<image>', methods=['GET', 'POST'])
def pipeline(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        utils.delete_images(app.config['OUTPUT_FOLDER_PIPELINES'])
        list_transformations = request.form.get('list_transformations').split(',')
        processing_lib.pipeline(filepath, list_transformations)
    original = ['/' + filepath, image]
    pipelines = utils.get_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    steps_count = utils.count_folders(app.config['OUTPUT_FOLDER_STEPS'])
    for index in range(1, steps_count + 1):
        if next((x for x in pipelines if int(x[1].split('-')[0]) == index), None) is None:
            pipelines.append(('/static/img/fail.gif', '{}-{}'.format(index, str(uuid.uuid4()).split('-')[0])))
    pipelines.sort(key=lambda x: int(x[1].split('-')[0]))
    return render_template('pipeline.html', original=original, pipelines=pipelines)


@app.route('/ocr/<image>', methods=['POST'])
def get_ocr(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return redirect(url_for('index'))
    text = request.form.get('text', '')
    pipelines = utils.get_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    pipelines.sort(key=lambda x: int(x[1].split('-')[0]))
    results = []
    for pipeline in pipelines:
        result_text, percentage = ocr.compare(text, utils.get_filepath(app.config['OUTPUT_FOLDER_PIPELINES'], pipeline[1]))
        results.append({'pipeline': pipeline[1].split('-')[0], 'original': text, 'result': result_text, 'percentage': percentage})
    results = sorted(results, key=itemgetter('percentage'), reverse=True)

    result_text, percentage = ocr.compare(text, filepath)
    results.insert(0, {'pipeline': 'original', 'original': text, 'result': result_text, 'percentage': percentage})
    return jsonify(results)


@app.route('/ocr-transformations/<image>', methods=['POST'])
def get_ocr_transformations(image):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], image)
    if filepath is None:
        return redirect(url_for('index'))
    text = request.form.get('text', '')
    transformations = utils.get_images(app.config['OUTPUT_FOLDER'])
    results = []
    for transformation in transformations:
        result_text, percentage = ocr.compare(text, utils.get_filepath(app.config['OUTPUT_FOLDER'], transformation[1]))
        results.append({'transformation': transformation[1].split('-')[0], 'original': text, 'result': result_text, 'percentage': percentage})
    results = sorted(results, key=itemgetter('percentage'), reverse=True)

    result_text, percentage = ocr.compare(text, filepath)
    results.insert(0, {'transformation': 'original', 'original': text, 'result': result_text, 'percentage': percentage})
    return jsonify(results)


@app.route('/steps/<original>/<folder>/', methods=['GET'])
def steps(original, folder):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], original)
    if filepath is None:
        return redirect(url_for('index'))
    original = ['/' + filepath, original]
    steps = utils.get_images('static/img/pipelines/steps/{}'.format(folder))
    steps.sort(key=lambda x: int(x[1].split(')')[0]))
    return render_template('steps.html', original=original, steps=steps, folder=folder)


@app.route('/ocr-steps/<original>/<folder>', methods=['POST'])
def get_ocr_steps(original, folder):
    filepath = utils.get_filepath(app.config['INPUT_FOLDER'], original)
    if filepath is None:
        return redirect(url_for('index'))
    text = request.form.get('text', '')
    steps = utils.get_images('static/img/pipelines/steps/{}'.format(folder))
    steps.sort(key=lambda x: int(x[1].split(')')[0]))
    results = []
    for step in steps:
        result_text, percentage = ocr.compare(text, utils.get_filepath('static/img/pipelines/steps/{}'.format(folder), step[1]))
        results.append({'step': step[1].split('-')[0], 'original': text, 'result': result_text, 'percentage': percentage})

    result_text, percentage = ocr.compare(text, filepath)
    results.insert(0, {'step': 'original', 'original': text, 'result': result_text, 'percentage': percentage})
    return jsonify(results)


if __name__ == "__main__":
    context = ('/etc/letsencrypt/live/loencontre.co/fullchain.pem', '/etc/letsencrypt/live/loencontre.co/privkey.pem')
    app.run(host='0.0.0.0', debug=False, port=3000, ssl_context=context)
