from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
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
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '100carbook'
app.config['MYSQL_DB'] = 'pythonlogin'

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf15hYbAAAAAK_KyjqVXkqKhFe6NUt-4HpzAIek'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf15hYbAAAAAMq2XaVag56w4fFCNmSo9WkgxOBh'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
app.config['RECAPTCHA_PARAMETERS '] = {'hl': 'pt'}


mysql = MySQL(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.form['btn'] == "login_btn":
            return redirect(url_for("authenticate"))

    return render_template('login.html')

@app.route("/authenticate", methods=['GET', 'POST'])
def authenticate():
    return render_template('authenticate.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run()
