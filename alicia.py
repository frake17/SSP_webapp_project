from url_jumping import check_role
import shelve

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import MySQLdb.cursors
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from random import randint
from datetime import datetime, timedelta
from datetime import timedelta, time
from twilio.rest import Client
import User
from Forms import CreateUserForm, SearchUserForm, AuthenticateLogin

UPLOAD_FOLDER = 'static/img/uploaded'
ALLOWED_EXTENSIONS = {'png'}

alicia = Flask(__name__)
alicia.secret_key = 'any_random_string'
alicia.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
alicia.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
alicia.config["SESSION_PERMANENT"] = False
alicia.config['MYSQL_HOST'] = 'localhost'
alicia.config['MYSQL_USER'] = 'root'
alicia.config['MYSQL_PASSWORD'] = '100carbook'
alicia.config['MYSQL_DB'] = 'pythonlogin'
alicia.config['MYSQL_PASSWORD'] = 'Singaporemysql1'
alicia.config['MYSQL_DB'] = 'ssp'
alicia.config['MAIL_SERVER'] = 'smtp.gmail.com'
alicia.config['MAIL_PORT'] = 465
alicia.config['MAIL_USERNAME'] = 'sspproject405@gmail.com'
alicia.config['MAIL_PASSWORD'] = 'SSP123456'
alicia.config['MAIL_USE_TLS'] = False
alicia.config['MAIL_USE_SSL'] = True
mysql = MySQL(alicia)
mail = Mail(alicia)
alicia = Blueprint('alicia', __name__, template_folder='templates')


@alicia.route('/temp_record', methods=['GET', 'POST'])
def create_user():
    if not check_role('Staff'):
        return redirect(url_for('home'))
    create_user_form = CreateUserForm(request.form)

    locations_dict = {}
    db = shelve.open('location.db', 'r')
    locations_dict = db['Locations']
    db.close()

    locations_list = []
    for key in locations_dict:
        location = locations_dict.get(key)
        locations_list.append(location)

    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        count_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users_temp']
            count_dict = db['Count']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User.Temp(request.form['location'], create_user_form.date.data,
                         create_user_form.cust_ic.data, create_user_form.cust_no.data,
                         create_user_form.temp.data,
                         create_user_form.time_enter.data, create_user_form.time_leave.data, 'in')
        users_dict[user.get_user_id()] = user
        db['Users_temp'] = users_dict

        session['user_created'] = user.get_cust_ic()

        print(request.form['location'], count_dict)
        if request.form['location'] in count_dict:
            count = count_dict.get(request.form['location'])
            count += 1
            count_dict[request.form['location']] = count
        else:
            count_dict[request.form['location']] = 1

        db['Count'] = count_dict

        db.close()

        return redirect(url_for('alicia.create_user'))
    return render_template('temp_record.html', form=create_user_form, locations_list=locations_list)


@alicia.route('/temp_search_user', methods=['GET', 'POST'])
def search_user():
    if not check_role('Deliveryman'):
        return redirect(url_for('home'))
    search_user_form = SearchUserForm(request.form)
    search_list = []
    count = 0
    db = shelve.open('location.db', 'r')
    locations_dict = db['Locations']
    db.close()
    db = shelve.open('storage.db', 'c')

    locations_list = []
    for key in locations_dict:
        location = locations_dict.get(key)
        locations_list.append(location)

    if request.method == "POST":
        users_dict = {}

        try:
            users_dict = db['Users_temp']
            db.close()

        except IOError:
            print("An error occurred trying to read from storage.db")

        except:
            print("An unknown error has occurred")

        if request.form['btn'] == "Retrieve":
            for key in users_dict:
                search = users_dict.get(key)
                if request.form['location'] == search.get_outlet():
                    if search_user_form.search_date.data == search.get_date():
                        search_list.append(search)

                        count = 0
                        for a in search_list:
                            if a.get_status() == "in":
                                count += 1

        elif request.form['btn'] == "Search":
            for key in users_dict:
                search = users_dict.get(key)
                if search_user_form.search_cust.data == search.get_cust_ic():
                    search_list.append(search)

    return render_template('temp_search_user.html', form=search_user_form, search_list=search_list, count=count,
                           locations_list=locations_list)


@alicia.route('/temp_updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}

        try:
            db = shelve.open('storage.db', 'w')
            users_dict = db['Users_temp']

        except IOError:
            print("An error occurred trying to write in storage.db")

        except:
            print("An unknown error has occurred")

        user = users_dict.get(id)
        user.set_date(update_user_form.date.data)
        user.set_cust_ic(update_user_form.cust_ic.data)
        user.set_cust_no(update_user_form.cust_no.data)
        user.set_temp(update_user_form.temp.data)
        user.set_time_enter(update_user_form.time_enter.data)
        user.set_time_leave(update_user_form.time_leave.data)
        user.set_status("left")

        db['Users_temp'] = users_dict
        db.close()

        session['user_updated'] = user.get_cust_ic()

        return redirect(url_for('alicia.search_user'))

    else:
        users_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users_temp']
            db.close()

        except IOError:
            print("An error occurred trying to read from storage.db")

        except:
            print("An unknown error has occurred")

        user = users_dict.get(id)
        update_user_form.date.data = user.get_date()
        update_user_form.cust_ic.data = user.get_cust_ic()
        update_user_form.cust_no.data = user.get_cust_no()
        update_user_form.temp.data = user.get_temp()
        update_user_form.time_enter.data = user.get_time_enter()
        update_user_form.time_leave.data = user.get_time_leave()
        user.get_status()

        return render_template('temp_updateUser.html', form=update_user_form)


@alicia.route('/temp_chart')
def temp_chart():
    locations_dict = {}
    locations_db = shelve.open('location.db', 'r')
    locations_dict = locations_db['Locations']
    locations_db.close()

    locations_label = []
    for line in locations_dict:
        location = locations_dict.get(line)
        locations_label.append(location.get_address())
    print(locations_label)

    count_dict = {}
    count_db = shelve.open('storage.db', 'r')
    count_dict = count_db['Count']
    print(count_dict)
    count_db.close()

    for location in locations_label:
        if location not in count_dict:
            count = 0
            count_dict[location] = count

    count_data = []
    for k in count_dict:
        count_data.append(count_dict[k])

    return render_template('chart.html', locations_label=locations_label, count_data=count_data)


@alicia.route("/authenticate", methods=['GET', 'POST'])  # SSP CODES DONE BY ALICIA
def authenticate():
    session.pop('reattemptTime', None)

    msg = ''

    if request.method == "POST":
        # Send authentication code to email

        if request.form.get('authEmail'):
            gen_auth_code = randint(100000, 999999)
            session['gen_auth_code'] = gen_auth_code
            print('code:', gen_auth_code)
            email = session.get('email')
            content = Message('Sheng Siong Supermarket Login', sender='smtp.gmail.com', recipients=[email])
            content.body = "Your login authentication code is %d" % gen_auth_code
            mail.send(content)

            session['sendAuth'] = True
            session['code method'] = 'email'

            time_start = datetime.now()
            duration = timedelta(minutes=3)
            expire_time = time_start + duration
            session['expire_time'] = expire_time
            time_format = expire_time.strftime('%H:%M')
            msg = 'Your authentication code will expire at %s' % time_format

        # Send authentication code to SMS
        elif request.form.get('authSMS'):
            gen_auth_code = randint(100000, 999999)
            session['gen_auth_code'] = gen_auth_code
            account_sid = 'ACd79f39ac30b9742e43c153ea68a04918'
            auth_token = '40520b503bb15b03ab4e71093eb084b3'
            client = Client(account_sid, auth_token)
            phone_num = str(session.get('phone_num'))
            print(gen_auth_code)

            message = client.messages \
                .create(
                body="Your login authentication code is %d" % gen_auth_code,
                from_='+19044743219',
                to='+65' + phone_num
            )

            print(message.sid)
            session['sendAuth'] = True
            session['code method'] = 'sms'

            time_start = datetime.now()
            duration = timedelta(minutes=3)
            expire_time = time_start + duration
            session['expire_time'] = expire_time
            time_format = expire_time.strftime('%H:%M')
            msg = 'Your authentication code will expire at %s' % time_format

        if request.form.get('submit_auth'):
            enter_code = int(request.form['auth_code'])
            time_click = datetime.now()
            if time_click.replace(tzinfo=None) > session.get('expire_time').replace(tzinfo=None):
                print("Authentication code expired")
                msg = 'Your authentication code has expired, please login again'
                return redirect(url_for('alicia.login'))

            else:
                print("Auth code:", session.get('gen_auth_code'))
                print("Entered code:", enter_code)
                if enter_code == session.get('gen_auth_code'):
                    print("Success")

                    role = session.get('pre_role')
                    session['role'] = role
                    session.pop('expire_time', None)
                    session.pop('gen_auth_code', None)
                    session.pop('sendAuth', None)
                    return redirect(url_for('home'))

                else:
                    msg = 'You have entered an invalid authentication code'
                    print("Wrong auth code")
                    session.pop('expire_time', None)
                    session.pop('gen_auth_code', None)
                    session.pop('sendAuth', None)
                    return redirect(url_for('elly.login'))

    return render_template('authenticate.html', msg=msg, form=AuthenticateLogin)


@alicia.route('/resend_code', methods=['GET', 'POST'])
def resend_code():
    gen_auth_code = randint(100000, 999999)
    session['gen_auth_code'] = gen_auth_code

    if session.get('sendAuth') == True:
        if session.get('code method') == "email":
            email = session.get('email')
            content = Message('Sheng Siong Supermarket Login', sender='smtp.gmail.com', recipients=[email])
            content.body = "Your new login authentication code is %d" % session.get('gen_auth_code')
            mail.send(content)

            session['sendAuth'] = True

        elif session.get('code method') == 'sms':
            account_sid = 'ACd79f39ac30b9742e43c153ea68a04918'
            auth_token = '40520b503bb15b03ab4e71093eb084b3'
            client = Client(account_sid, auth_token)
            phone_num = str(session.get('phone_num'))

            message = client.messages \
                .create(
                body="Your new login authentication code is %d" % gen_auth_code,
                from_='+19044743219',
                to='+65' + phone_num
            )

            print(message.sid)
            session['sendAuth'] = True

        time_start = datetime.now()
        duration = timedelta(minutes=3)
        expire_time = time_start + duration
        session['expire_time'] = expire_time
        time_format = expire_time.strftime('%H:%M')
        msg = 'Your new authentication code will expire at %s' % time_format
        #return redirect(url_for('alicia.authenticate'))

    else:
        msg = 'You have not chosen a method to send your authentication code'

    return render_template(url_for('/alicia.authenticate'), msg=msg)


