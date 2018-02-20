from flask import Flask, render_template, request, url_for, redirect
from os import listdir
from os.path import join

UPLOAD_FOLDER = 'static/img/input/'
ALLOWED_EXTENSIONS = set(['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    images = [(join(app.config['UPLOAD_FOLDER'], file), file.split('.')[0]) for file in listdir(app.config['UPLOAD_FOLDER']) if allowed_file(file)]
    if request.method == 'POST':
        new_file = request.files['file']
        if new_file and allowed_file(new_file.filename):
            filename = str(len(images) + 1) + '.' + new_file.filename.rsplit('.', 1)[1].lower()
            new_file.save(join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('index.html', images=images)


if __name__ == "__main__":
    app.run(debug=True)
