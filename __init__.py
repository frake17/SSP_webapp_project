from flask import Flask, render_template

from alicia import alicia
from elly import elly
from kin import kin
from zhiching import qing

UPLOAD_FOLDER = 'static/img/uploaded'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.secret_key = 'any_random_string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SESSION_PERMANENT"] = False
app.register_blueprint(alicia)
app.register_blueprint(elly)
app.register_blueprint(kin)
app.register_blueprint(qing)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run()
