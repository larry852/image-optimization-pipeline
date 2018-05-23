from flask import Flask, render_template, request, url_for, redirect
from os.path import join
from core import main as processing_lib
import utils


app = Flask(__name__)
app.config['INPUT_FOLDER'] = 'static/img/input/'
app.config['OUTPUT_FOLDER'] = 'static/img/output/'
app.config['OUTPUT_FOLDER_PIPELINES'] = 'static/img/pipelines/results'


@app.route('/', methods=['GET', 'POST'])
def index():
    images = utils.get_images(app.config['INPUT_FOLDER'])
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
        return redirect(url_for('pipeline', image=image))
    original = ['/' + filepath, image]
    transformations = utils.get_images(app.config['OUTPUT_FOLDER_PIPELINES'])
    return render_template('pipeline.html', original=original, transformations=transformations)


if __name__ == "__main__":
    app.run(debug=True)
