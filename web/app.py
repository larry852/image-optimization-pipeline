from flask import Flask, render_template, request, url_for, redirect
from os import listdir
from os.path import isfile, join
import imghdr

app = Flask(__name__)


@app.route('/')
def index():
    images_path = 'static/img/input/'
    images = [join(images_path, file) for file in listdir(images_path) if isfile(join(images_path, file)) and imghdr.what(join(images_path, file))]
    return render_template('index.html', images=images)


if __name__ == "__main__":
    app.run(debug=True)
