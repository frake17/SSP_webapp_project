import shelve

from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint

import Location
import User
from Forms import SignUp, Login, CreateLocation, UpdateProfile, UpdatePassword, optional_signup, recaptcha_form
# SSP CODES
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_recaptcha import ReCaptcha
import requests
import json
from flask_mail import Mail, Message
import bcrypt
from random import randint
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from twilio.rest import Client
import random
import string

elly = Flask(__name__)
elly.secret_key = 'any_random_string'
elly.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
elly.config["SESSION_PERMANENT"] = False

# SSP CODES
elly.config['MAIL_SERVER'] = 'smtp.gmail.com'
elly.config['MAIL_PORT'] = 465
elly.config['MAIL_USERNAME'] = 'sspproject405@gmail.com'
elly.config['MAIL_PASSWORD'] = 'SSP123456'
elly.config['MAIL_USE_TLS'] = False
elly.config['MAIL_USE_SSL'] = True
elly.config['MYSQL_HOST'] = 'localhost'
elly.config['MYSQL_USER'] = 'root'
elly.config['MYSQL_PASSWORD'] = '100carbook'
elly.config['MYSQL_DB'] = 'pythonlogin'
recaptcha = ReCaptcha(app=elly)
mysql = MySQL(elly)
mail = Mail(elly)
elly = Blueprint('elly', __name__, template_folder='templates', static_folder='static')


def polynomialRollingHash(str):  # To hash string
    # P and M
    p = 31
    m = 1e9 + 9
    power_of_p = 1
    hash_val = 0

    # Loop to calculate the hash value
    # by iterating over the elements of string
    for i in range(len(str)):
        hash_val = ((hash_val + (ord(str[i]) -
                                 ord('a') + 1) *
                     power_of_p) % m)

        power_of_p = (power_of_p * p) % m

    return int(hash_val)


@elly.route('/loginActivity(cust)')
def loginActivity():
    return render_template('loginActivity(cust).html')


@elly.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUp(request.form)
    optional_form = optional_signup(request.form)
    recaptcha_forms = recaptcha_form(request.form)
    if request.method == 'POST' and signup_form.validate():
        if request.method == 'POST' and signup_form.validate() and optional_form.validate():

            # users_dict = {}
            # db = shelve.open('storage.db', 'c')

            # users_list = []
            # for key in users_dict:
            #    user = users_dict.get(key)
            #    if key == signup_form.email.data:
            #        flash("Account already exist")
            #        return redirect(url_for('home'))

            # try:
            #    users_dict = db['Users']
            # except:
            #    print("Error in retrieving Users from storage.db.")

            # user = User.User(signup_form.first_name.data, signup_form.last_name.data, signup_form.email.data,
            #                signup_form.password.data)
            # print("===user====", user)
            # users_dict[user.get_email()] = user
            # db['Users'] = users_dict

            # Test codes
            # users_dict = db['Users']

            # user = users_dict[user.get_email()]
            # print(user.get_first_name(), user.get_last_name(), "was stored in storage.db successfully with user_id ==",
            #      user.get_user_id())

            # db.close()

            # session['user_created'] = user.get_first_name() + ' ' + user.get_last_name()

            # MySQL SSP Codes
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                              data={'secret':
                                        '6Lf15hYbAAAAAMq2XaVag56w4fFCNmSo9WkgxOBh',
                                    'response':
                                        request.form['g-recaptcha-response']})

            google_response = json.loads(r.text)
            print('JSON: ', google_response)

            if google_response['success']:

                # if optional_form.Phone_number.data != '' or optional_form.Phone_number.data is not None:
                if optional_form.Phone_number.data is not None:
                    phone_key = Fernet.generate_key()
                    f = Fernet(phone_key)
                    encrypted_phone_num = f.encrypt(str(optional_form.Phone_number.data).encode())
                    phone_num = encrypted_phone_num
                else:
                    phone_num = 'NULL'
                    phone_key = 'NULL'

                # if optional_form.card_number.data != '' or optional_form.card_number.data is not None:
                if optional_form.card_number.data is not None:
                    Card_num_key = Fernet.generate_key()
                    f = Fernet(Card_num_key)
                    encrypted_card_num = f.encrypt(str(optional_form.card_number.data).encode())
                    card_num = encrypted_card_num
                else:
                    card_num = 'NULL'
                    Card_num_key = 'NULL'

                # if optional_form.exp_date.data != '' or optional_form.exp_date.data is not None:
                if optional_form.exp_date.data is not None:
                    Card_exp_key = Fernet.generate_key()
                    f = Fernet(Card_exp_key)
                    encrypted_card_exp = f.encrypt(str(optional_form.card_number.data).encode())
                    exp_date = encrypted_card_exp
                else:
                    exp_date = 'NULL'
                    Card_exp_key = 'NULL'

                # if optional_form.CVV.data != '' or optional_form.CVV.data is not None:
                if optional_form.CVV.data is not None:
                    Card_cvv_key = Fernet.generate_key()
                    f = Fernet(Card_cvv_key)
                    encrypted_card_cvv = f.encrypt(str(optional_form.CVV.data).encode())
                    CVV = encrypted_card_cvv
                else:
                    CVV = 'NULL'
                    Card_cvv_key = 'NULL'

                # conformation_code = randint(000000, 999999)
                first_name = signup_form.first_name.data
                last_name = signup_form.last_name.data
                email = signup_form.email.data
                password = signup_form.password.data
                security_qn = signup_form.security_question.data
                security_ans = signup_form.security_answer.data
                # Password Hashing
                # Create a random number (Salt)
                salt = bcrypt.gensalt(rounds=16)
                # A hashed value is created with hashpw() function, which takes the cleartext value and a salt as
                # parameters.
                hash_password = bcrypt.hashpw(password.encode(), salt)
                hash_security_ans = polynomialRollingHash(security_ans)

                # Symmetric Key Encryption
                # Generate a random Symmetric key. Keep this key in your database
                key = Fernet.generate_key()
                # Load the key into the Crypto API
                f = Fernet(key)
                # Encrypt the email and convert to bytes by calling f.encrypt()
                encryptedEmail = f.encrypt(email.encode())

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(
                    'INSERT INTO customers_temp VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (first_name, last_name, encryptedEmail, hash_password, phone_num, card_num, exp_date, CVV,
                     security_qn, hash_security_ans, key, phone_key, Card_num_key, Card_exp_key, Card_cvv_key))
                mysql.connection.commit()
                session['fname'] = first_name
                session['lname'] = last_name
                session['EMAIL'] = email
                # session['code'] = conformation_code
                session['code_sent'] = False
                session['Phone Number'] = optional_form.Phone_number.data

                return redirect(url_for('elly.signup_confirmation'))

    return render_template('signup(customer).html', form=signup_form, optional_form=optional_form,
                           recap=recaptcha_forms)


@elly.route('/send_email', methods=['GET', 'POST'])  # SSP CODE
def send_email():
    email = session.get('EMAIL')
    conformation_code = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(12)])
    current_time = datetime.now()
    session['code'] = conformation_code
    session['date'] = current_time

    msg = Message('Hello', sender='smtp.gmail.com', recipients=[email])
    msg.body = "Conformation code is: %d" % conformation_code
    mail.send(msg)
    session['code_sent'] = True
    return redirect(url_for('elly.signup_confirmation'))


@elly.route('/send_sms', methods=['GET', 'POST'])  # SSP CODE
def send_sms():
    account_sid = 'ACd79f39ac30b9742e43c153ea68a04918'
    auth_token = '40520b503bb15b03ab4e71093eb084b3'
    client = Client(account_sid, auth_token)
    phone_num = str(session.get('Phone Number'))
    conformation_code = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(12)])
    current_time = datetime.now()
    session['code'] = conformation_code
    session['date'] = current_time

    message = client.messages \
        .create(
        body="Conformation code is: %d" % conformation_code,
        from_='+19044743219',
        to='+65' + phone_num
    )

    print(message.sid)
    session['code_sent'] = True
    return redirect(url_for('elly.signup_confirmation'))


@elly.route('/signup_confirmation', methods=['GET', 'POST'])  # SSP CODE
def signup_confirmation():
    time_change = timedelta(minutes=15)
    date = session.get('date')
    Changed_time = date + time_change
    first_name = session['fname']
    last_name = session['lname']
    status = session.get('code_sent', False)
    conformation_code = session.get('code')

    if request.method == 'POST' and status == True:
        code = request.form['confirmation']
        if int(code) == int(conformation_code):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO customers SELECT * FROM customers_temp WHERE fname = %s and lname = %s'
                           , (first_name, last_name))
            cursor.execute('DELETE FROM customers_temp WHERE fname = %s and lname = %s', (first_name, last_name))
            mysql.connection.commit()
            session['customer'] = True
            session['admin'] = False
            session['deliveryman'] = False
            session['HR'] = False
            session['code'] = ''
            session['code_sent'] = False
            return redirect(url_for('elly.account_created'))
        elif datetime.now() < Changed_time:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('DELETE FROM customers_temp WHERE fname = %s and lname = %s', (first_name, last_name))
            mysql.connection.commit()
            session['code'] = ''
            session['code_sent'] = False
            session['Code expire'] = 'Authentication code is expired, please sign up again'
            return redirect(url_for('elly.signup'))
        else:
            session['Wrong Code'] = 'You have inputted the wrong code'
            return redirect(url_for('elly.signup_confirmation'))
    return render_template('Signup_confirmation.html')


@elly.route('/resend', methods=['POST', 'GET'])
def resend():
    current_time = datetime.now()
    email = session.get('EMAIL')
    conformation_code = randint(000000, 999999)
    msg = Message('Hello', sender='smtp.gmail.com', recipients=[email])
    msg.body = "Conformation code is: %d" % conformation_code
    mail.send(msg)

    return redirect(url_for('elly.signup_confirmation', conformation_code=conformation_code, date=current_time))


@elly.route('/Account_created', methods=['GET', 'POST'])
def account_created():
    first_name = session.get('fname')
    last_name = session.get('lname')
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('Account_created.html', fname=first_name, lname=last_name)


@elly.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        users_dict = db['Users']
    except:
        print('no users')
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers(admin).html', count=len(users_list), users_list=users_list)


@elly.route('/deleteUser/<email>', methods=['POST'])
def delete_user(email):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(email)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('elly.retrieve_users'))


@elly.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login(request.form)
    if request.method == 'POST' and login_form.validate():
        session['current'] = login_form.email.data
        if login_form.email.data == "ss_staff@gmail.com":
            if login_form.password.data == "Admin123":
                session['admin'] = True
                session['customer'] = False
                session['deliveryman'] = False
                return redirect(url_for('home'))
            else:
                session['customer'] = False
                session['admin'] = False
                session['deliveryman'] = False
        else:
            users_dict = {}
            deliveryman_login = {}
            db = shelve.open('storage.db', 'r')
            try:
                users_dict = db['Users']
            except:
                return redirect(url_for('elly.signup'))
            try:
                deliveryman_login = db["Deliverymen_login"]
            except:
                print('no deliveryman')
            db.close()

            users_list = []
            for key in deliveryman_login:
                if login_form.email.data == key:
                    print('dsa')
                    if login_form.password.data == 'Deliverymen123':
                        session['customer'] = False
                        session['admin'] = False
                        session['deliveryman'] = True
                        return redirect(url_for('home'))
            for key in users_dict:
                user = users_dict.get(key)
                if key == login_form.email.data:
                    if login_form.password.data == user.get_password():
                        users_list.append(user)
                        session['customer'] = True
                        session['admin'] = False
                        session['deliveryman'] = False
                        return redirect(url_for('elly.profile'))
            if login_form.email.data not in users_dict:
                return redirect(url_for('elly.signup'))

    return render_template('login.html', form=login_form)  # change to login.html


@elly.route('/logout')
def logout():
    try:
        session.pop('current', None)
        session.pop('admin', None)
        session.pop('customer', None)
        session.pop('deliverman', None)
    except:
        flash('User is not logged in')
    return redirect(url_for('home'))


@elly.route('/profile')
def profile():
    email = session.get('current', 'c')
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        if key == email:
            users_list.append(user)

    return render_template('profile(customer).html', count=len(users_list), users_list=users_list)


@elly.route('/deleteAcc/<email>', methods=['POST'])
def delete_acc(email):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(email)

    db['Users'] = users_dict
    db.close()

    try:
        session.pop('current', None)
        session.pop('customer', None)
    except:
        flash('User is not logged in')
    return redirect(url_for('home'))


@elly.route('/updateProfile/<email>/', methods=['GET', 'POST'])
def update_profile(email):
    update_profile_form = UpdateProfile(request.form)
    if request.method == 'POST' and update_profile_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(email)
        user.set_first_name(update_profile_form.first_name.data)
        user.set_last_name(update_profile_form.last_name.data)
        user.set_email(update_profile_form.email.data)
        db['Users'] = users_dict
        db.close()

        return redirect(url_for('elly.profile'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(email)
        update_profile_form.first_name.data = user.get_first_name()
        update_profile_form.last_name.data = user.get_last_name()
        update_profile_form.email.data = user.get_email()
        return render_template('updateProfile.html', form=update_profile_form)


@elly.route('/updatePassword/<email>/', methods=['GET', 'POST'])
def update_password(email):
    update_password_form = UpdatePassword(request.form)
    if request.method == 'POST' and update_password_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(email)
        user.set_password(update_password_form.password.data)
        db['Users'] = users_dict
        db.close()

        return redirect(url_for('elly.profile'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(email)
        update_password_form.password.data = user.get_password()
        return render_template('updatePassword(cust).html', form=update_password_form)


@elly.route('/createLocation', methods=['GET', 'POST'])
def create_location():
    location_form = CreateLocation(request.form)
    count = 1
    if request.method == 'POST' and location_form.validate():
        locations_dict = {}
        db = shelve.open('location.db', 'c')

        try:
            locations_dict = db['Locations']
            while count in locations_dict:
                count += 1
        except:
            print("Error in retrieving locations from location.db.")

        location = Location.Location(location_form.neighbourhood.data, location_form.address.data,
                                     location_form.area.data, location_form.availability.data)
        print("===location====", location)
        location.set_location_id(count)
        locations_dict[location.get_location_id()] = location
        db['Locations'] = locations_dict

        # Test codes
        locations_dict = db['Locations']
        location = locations_dict[location.get_location_id()]
        print(location.get_address(), "was stored in location.db successfully with location_id ==",
              location.get_location_id())

        db.close()

        session['location_created'] = location.get_address()

        return redirect(url_for('elly.retrieve_locations'))
    return render_template('createLocation(admin).html', form=location_form)


@elly.route('/retrieveLocations')
def retrieve_locations():
    locations_dict = {}
    db = shelve.open('location.db', 'r')
    locations_dict = db['Locations']
    db.close()

    locations_list = []
    for key in locations_dict:
        location = locations_dict.get(key)
        locations_list.append(location)

    return render_template('retrieveLocations(admin).html', count=len(locations_list), locations_list=locations_list)


@elly.route('/storeLocator')
def store_locator():
    locations_dict = {}
    try:
        db = shelve.open('location.db', 'r')
        locations_dict = db['Locations']
        db.close()
    except:
        print('location no created')

    locations_list = []
    for key in locations_dict:
        location = locations_dict.get(key)
        locations_list.append(location)

    return render_template('storeLocator(customer).html', count=len(locations_list), locations_list=locations_list)


@elly.route('/deleteLocation/<int:id>', methods=['POST'])
def delete_location(id):
    locations_dict = {}
    db = shelve.open('location.db', 'w')
    locations_dict = db['Locations']

    locations_dict.pop(id)

    db['Locations'] = locations_dict
    db.close()

    return redirect(url_for('elly.retrieve_locations'))


@elly.route('/updateLocation/<int:id>/', methods=['GET', 'POST'])
def update_location(id):
    update_location_form = CreateLocation(request.form)
    if request.method == 'POST' and update_location_form.validate():
        locations_dict = {}
        db = shelve.open('location.db', 'w')
        locations_dict = db['Locations']

        location = locations_dict.get(id)
        location.set_neighbourhood(update_location_form.neighbourhood.data)
        location.set_address(update_location_form.address.data)
        location.set_area(update_location_form.area.data)
        location.set_availability(update_location_form.availability.data)
        db['Locations'] = locations_dict
        db.close()

        return redirect(url_for('elly.retrieve_locations'))
    else:
        locations_dict = {}
        db = shelve.open('location.db', 'r')
        locations_dict = db['Locations']
        db.close()

        location = locations_dict.get(id)
        update_location_form.neighbourhood.data = location.get_neighbourhood()
        update_location_form.address.data = location.get_address()
        update_location_form.area.data = location.get_area()
        update_location_form.availability.data = location.get_availability()
        return render_template('updateLocation(admin).html', form=update_location_form)
