from flask import Flask, render_template, request, url_for, redirect
from os import listdir, unlink
from os.path import join, dirname, abspath
from core import main as processing_lib

INPUT_FOLDER = 'static/img/input/'
OUTPUT_FOLDER = 'static/img/output/'
ALLOWED_EXTENSIONS = set(['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr', 'jpg'])

app = Flask(__name__)
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    images = [('/' + join(app.config['INPUT_FOLDER'], file), file.split('.')[0]) for file in listdir(app.config['INPUT_FOLDER']) if allowed_file(file)]
    if request.method == 'POST':
        new_file = request.files['file']
        if new_file and allowed_file(new_file.filename):
            filename = str(len(images) + 1) + '.' + new_file.filename.rsplit('.', 1)[1].lower()
            new_file.save(join(app.config['INPUT_FOLDER'], filename))
            return redirect(url_for('processing', image=filename.split('.')[0]))
    return render_template('index.html', images=images)


@app.route('/processing/<image>')
def processing(image):
    try:
        filepath = [join(app.config['INPUT_FOLDER'], file) for file in listdir(app.config['INPUT_FOLDER']) if file.split('.')[0] == image][0]
    except Exception:
        return redirect(url_for('index'))

    for file in listdir(app.config['OUTPUT_FOLDER']):
        unlink(dirname(abspath(file)) + '/' + join(app.config['OUTPUT_FOLDER'], file))

    processing_lib.main(filepath)
    original = ['/' + filepath, image]
    transformations = [('/' + join(app.config['OUTPUT_FOLDER'], file), file.split('.')[0]) for file in listdir(app.config['OUTPUT_FOLDER']) if allowed_file(file)]
    return render_template('processing.html', original=original, transformations=transformations)


if __name__ == "__main__":
    app.run(debug=True)
