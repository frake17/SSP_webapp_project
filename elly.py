import shelve

from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint

import Location
import User
from Forms import SignUp, Login, CreateLocation, UpdateProfile, UpdatePassword, optional_signup, recaptcha_form, \
    UpdatePassword, ForgetPassword, PwSecurity, FindEmail
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
from url_jumping import check_role  # SSP CODE DONE BY KIN

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


def polynomialRollingHash(str):  # SSP CODE DONE BY KIN : To hash string
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


@elly.route('/loginActivity(cust)')  # SSP CODE DONE BY ZHICHING
def loginActivity():
    # create a list
    users_list = []
    fname = session.get('fname')
    lname = session.get('lname')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM CustomerLoginActivity WHERE fname = %s and lname = %s", (fname, lname))
    account = cursor.fetchone()
    while account is not None:
        users_list.append(account)
        account = cursor.fetchone()
    return render_template('loginActivity(cust).html', users_list=users_list)


@elly.route('/signup', methods=['GET', 'POST'])  # SSP CODE DONE BY KIN
def signup():
    signup_form = SignUp(request.form)
    optional_form = optional_signup(request.form)
    recaptcha_forms = recaptcha_form(request.form)
    if request.method == 'POST' and signup_form.validate():
        if request.method == 'POST' and signup_form.validate() and optional_form.validate():

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
                    print('1')
                else:
                    phone_num = 'NULL'
                    phone_key = 'NULL'

                # if optional_form.card_number.data != '' or optional_form.card_number.data is not None:
                if optional_form.card_number.data is not None:
                    Card_num_key = Fernet.generate_key()
                    f = Fernet(Card_num_key)
                    encrypted_card_num = f.encrypt(str(optional_form.card_number.data).encode())
                    card_num = encrypted_card_num
                    print('2')
                else:
                    card_num = 'NULL'
                    Card_num_key = 'NULL'

                # if optional_form.exp_date.data != '' or optional_form.exp_date.data is not None:
                if optional_form.exp_date.data is not None:
                    Card_exp_key = Fernet.generate_key()
                    f = Fernet(Card_exp_key)
                    encrypted_card_exp = f.encrypt(str(optional_form.card_number.data).encode())
                    exp_date = encrypted_card_exp
                    print('3')
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
                status = ''

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM Customers')
                account = cursor.fetchone()
                while account is not None:  # RE-ENABLE ONCE DONE TESTING
                    fname = account['fname']
                    lname = account['lname']
                    key = account['symmetrickey']
                    f = Fernet(key)
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    decryptedEmail = decryptedEmail_Binary.decode()
                    if (fname == first_name and lname == last_name) or decryptedEmail == email:
                        status = 'User is registered'
                        break
                    account = cursor.fetchone()
                if status != 'User is registered':
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

                    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(
                        'INSERT INTO customers_temp VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (first_name, last_name, encryptedEmail, hash_password, phone_num, card_num, exp_date, CVV,
                         security_qn, hash_security_ans, key, phone_key, Card_num_key, Card_exp_key, Card_cvv_key))
                    mysql.connection.commit()
                    session['fname'] = first_name
                    session['lname'] = last_name
                    session['email'] = email
                    # session['code'] = conformation_code
                    session['code_sent'] = False
                    session['Phone Number'] = optional_form.Phone_number.data

                    return redirect(url_for('elly.signup_confirmation'))
                else:
                    session['registered'] = 'Name or email have been registered'

    return render_template('signup(customer).html', form=signup_form, optional_form=optional_form,
                           recap=recaptcha_forms)


@elly.route('/send_email', methods=['GET', 'POST'])  # SSP CODE DONE BY KIN
def send_email():
    email = session.get('email')
    conformation_code = randint(000000, 999999)
    current_time = datetime.now().replace(tzinfo=None)
    session['code'] = conformation_code
    session['date'] = current_time

    msg = Message('Sheng Siong Supermarket registration', sender='smtp.gmail.com', recipients=[email])
    msg.body = "Your registration authentication code: %d" % conformation_code
    mail.send(msg)
    session['code_sent'] = True
    return redirect(url_for('elly.signup_confirmation'))


@elly.route('/send_sms', methods=['GET', 'POST'])  # SSP CODE DONE BY KIN
def send_sms():
    account_sid = 'ACd79f39ac30b9742e43c153ea68a04918'
    auth_token = '40520b503bb15b03ab4e71093eb084b3'
    client = Client(account_sid, auth_token)
    phone_num = str(session.get('Phone Number'))
    conformation_code = randint(000000, 999999)
    current_time = datetime.now().replace(tzinfo=None)
    session['code'] = conformation_code
    session['date'] = current_time

    message = client.messages \
        .create(
        body="Your registration authentication code: %d" % conformation_code,
        from_='+19044743219',
        to='+65' + phone_num
    )

    print(message.sid)
    session['code_sent'] = True
    return redirect(url_for('elly.signup_confirmation'))


@elly.route('/signup_confirmation', methods=['GET', 'POST'])  # SSP CODE DONE BY KIN
def signup_confirmation():
    time_change = timedelta(minutes=1)
    first_name = session['fname']
    last_name = session['lname']
    status = session.get('code_sent', False)
    conformation_code = session.get('code')
    print(conformation_code)
    if request.method == 'POST' and status == True:
        date = session.get('date')
        Changed_time = date + time_change
        Changed_time = Changed_time.replace(tzinfo=None)
        code = request.form['confirmation']
        if datetime.now().replace(tzinfo=None) > Changed_time:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('DELETE FROM customers_temp WHERE fname = %s and lname = %s', (first_name, last_name))
            mysql.connection.commit()
            session['code'] = ''
            session['code_sent'] = False
            session['Code expire'] = 'Authentication code is expired, please sign up again'
            return redirect(url_for('elly.signup'))
        elif int(code) == int(conformation_code):
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
        else:
            session['Wrong Code'] = 'You have inputted the wrong code'
            return redirect(url_for('elly.signup_confirmation'))
    return render_template('Signup_confirmation.html')


@elly.route('/Account_created', methods=['GET', 'POST'])  # SSP CODE DONE BY KIN
def account_created():
    first_name = session.get('fname')
    last_name = session.get('lname')
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('Account_created.html', fname=first_name, lname=last_name)


@elly.route('/retrieveUsers')
def retrieve_users():
    if not check_role('Staff'):
        return redirect(url_for('home'))
    users_list = {}
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers')
    account = cursor.fetchone()
    while account is not None:
        key = account['symmetrickey']
        # Load the key
        f = Fernet(key)
        # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
        # using.encode()
        decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
        decryptedEmail = decryptedEmail_Binary.decode()
        users_list[decryptedEmail] = account
        account = cursor.fetchone()
    return render_template('retrieveUsers(admin).html', count=len(users_list), users_list=users_list)


@elly.route('/deleteUser/<email>', methods=['POST'])  # For staff
def delete_user(email):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers')
    account = cursor.fetchone()
    while account is not None:
        key = account['symmetrickey']
        encrypted_email = account['encrypted_email']
        # Load the key
        f = Fernet(key)
        # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
        # using.encode()
        decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
        decryptedEmail = decryptedEmail_Binary.decode()
        if email == decryptedEmail:
            fname = account['fname']
            lname = account['lname']
            cursor.execute('DELETE FROM Customers WHERE fname = %s and lname = %s', (fname, lname))
        account = cursor.fetchone()
    mysql.connection.commit()

    return redirect(url_for('elly.retrieve_users'))


@elly.route('/login', methods=['GET', 'POST'])  # SSP CODES DONE BY ALICIA
def login():
    msg = ''
    acct_exist = False
    if request.method == "POST" and 'email' in request.form and 'passwd' in request.form:
        email = request.form['email']
        passwd = request.form['passwd']
        # Check if account is in customers database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customers')
        cust_acct = cursor.fetchall()
        i = 0

        while i < len(cust_acct):
            for row in cust_acct:
                i += 1
                cust_key = row['symmetrickey']  # symmetrickey
                cust_f = Fernet(cust_key)
                cust_decryptedEmail_Binary = cust_f.decrypt(row['encrypted_email'].encode())  # encrypted_email
                cust_decryptedEmail = cust_decryptedEmail_Binary.decode()

                if email.lower() == cust_decryptedEmail.lower():
                    print("Account exist in database")

                    # Check if password is correct
                    cust_hashAndSalt = row['hashed_password']  # hashed_password
                    if bcrypt.checkpw(passwd.encode(), cust_hashAndSalt.encode()):
                        session['loggedin'] = True
                        session['email'] = cust_decryptedEmail.lower()
                        session['fname'] = row['fname']
                        session['lname'] = row['lname']
                        session['pre_role'] = 'Customer'
                        print("Password is correct")
                        acct_exist = True

                        res = requests.get("https://ipinfo.io/")
                        data = res.json()
                        location = data['city']
                        ipaddress = data['ip']
                        fname = row['fname']
                        lname = row['lname']
                        logout_time = '2021-08-08'
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        session['ipaddress'] = ipaddress
                        session['login_time'] = login_time
                        cursor.execute('INSERT INTO CustomerLoginActivity VALUES (NULL, %s, %s, %s, %s, %s, %s)',
                                       (fname, lname, login_time, location, ipaddress, logout_time))
                        mysql.connection.commit()

                        break

                    else:
                        msg = 'Wrong email / password entered'
                        print("Wrong password")
                        break

        # Check if account is in staff database
        else:
            cursor.execute('SELECT * FROM staff')
            staff_acct = cursor.fetchall()
            k = 0

            while k < len(staff_acct):
                for row in staff_acct:
                    k += 1
                    staff_key = row['symmetrickey']  # symmetrickey
                    staff_f = Fernet(staff_key)
                    staff_decryptedEmail_Binary = staff_f.decrypt(row['encrypted_email'].encode())  # encrypted_email
                    staff_decryptedEmail = staff_decryptedEmail_Binary.decode()
                    print(staff_decryptedEmail)

                    if email.lower() == staff_decryptedEmail.lower():
                        print("Account exist in database")

                        # Check if password is correct
                        staff_hashAndSalt = row['hashed_password']  # hashed_password
                        if bcrypt.checkpw(passwd.encode(), staff_hashAndSalt.encode()):
                            session['loggedin'] = True
                            session['email'] = staff_decryptedEmail.lower()
                            print("Password is correct")
                            acct_exist = True

                            role = row['role']
                            session['pre_role'] = role
                            print('pre role: ', session['pre_role'])

                            res = requests.get("https://ipinfo.io/")
                            data = res.json()
                            location = data['city']
                            ipaddress = data['ip']
                            fname = row['fname']
                            lname = row['lname']
                            logout_time = '2021-08-08'
                            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            session['ipaddress'] = ipaddress
                            session['login_time'] = login_time
                            cursor.execute('INSERT INTO StaffLoginActivity VALUES (NULL, %s, %s, %s, %s, %s, %s)',
                                           (fname, lname, login_time, location, ipaddress, logout_time))
                            mysql.connection.commit()
                            break

                        else:
                            msg = 'Wrong email / password entered'
                            print("Wrong password")
                            break

        if acct_exist == False:
            msg = 'Wrong email / password entered'
            print("Account does not exist in database")

        # Create the authentication code
        elif acct_exist == True:
            gen_auth_code = randint(100000, 999999)
            session['gen_auth_code'] = gen_auth_code

            # Send authentication code to email
            content = Message('Sheng Siong Supermarket Login', sender='smtp.gmail.com', recipients=[email])
            content.body = "Your login authentication code is %d" % gen_auth_code
            mail.send(content)

            time_start = datetime.now()
            duration = timedelta(minutes=3)
            expire_time = time_start + duration
            session['expire_time'] = expire_time

            return redirect(url_for('alicia.authenticate'))

    return render_template('login.html', msg=msg)


@elly.route('/findEmail', methods=['POST', 'GET'])  # SSP CODE DONE BY ELLY
def findEmail():
    msg = ''
    find_email = FindEmail(request.form)
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customers')
        account = cursor.fetchone()

        if account:
            key = account['symmetrickey']
            f = Fernet(key)
            decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
            decryptedEmail = decryptedEmail_Binary.decode()
            if decryptedEmail == email:
                session['email'] = True
                return redirect(url_for('elly.send_pwemail'))
    return render_template('findEmail(cust).html', msg='', form=find_email)


@elly.route('/send_pwemail', methods=['GET', 'POST'])  # SSP CODE DONE BY ELLY
def send_pwemail():
    email = session.get('EMAIL')
    current_time = datetime.now()
    session['date'] = current_time

    msg = Message('Hello', sender='smtp.gmail.com', recipients=[email])
    msg.body = 'Click link to update password' \
               ' http://127.0.0.1:5000/forgetPassword'
    mail.send(msg)
    session['link_sent'] = True
    session['email'] = True
    return redirect(url_for('elly.login'))


@elly.route('/forgetPassword', methods=['GET', 'POST'])  # SSP CODE DONE BY ELLY
def forgetPassword():
    fname = session.get('fname')
    lname = session.get('lname')
    if 'email' in session:
        if request.method == 'POST' and 'passwd' in request.form:
            newpassword = request.form['passwd']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            salt = bcrypt.gensalt(rounds=16)
            # A hashed value is created with hashpw() function, which takes the cleartext value and a salt as
            # parameters.
            hash_password = bcrypt.hashpw(newpassword.encode(), salt)
            cursor.execute('UPDATE Customers SET hashed_password = %s WHERE fname = %s and lname = %s',
                           (hash_password, fname, lname))
            mysql.connection.commit()
            return redirect(url_for('elly.login'))
        return render_template('forgetPassword(cust).html', msg='')


@elly.route('/logout')  # SSP CODE DONE BY ZHICHING
def logout():
    ipaddress = session.get('ipaddress')
    login_time = session.get('login_time')
    logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if session.get("role") == "Deliveryman" or session.get('role') == 'Staff' or session.get('role') == 'HR':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE StaffLoginActivity SET logout_time = %s WHERE ipaddress = %s AND login_time = %s",
                       (logout_time, ipaddress, login_time))
        mysql.connection.commit()
    elif session.get("role") == 'Customer':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE CustomerLoginActivity SET logout_time = %s WHERE ipaddress = %s AND login_time = %s",
                       (logout_time, ipaddress, login_time))
        mysql.connection.commit()
    try:
        session.pop('email', None)
        session.pop('role', None)
    except:
        flash('User is not logged in')
    return redirect(url_for('home'))


@elly.route('/profile')  # SSP CODE DONE BY ELLY
def profile():
    users_list = {}
    if 'email' in session:
        email = session.get('email')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customers')
        account = cursor.fetchone()
        while account is not None:
            key = account['symmetrickey']
            f = Fernet(key)
            decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
            decryptedEmail = decryptedEmail_Binary.decode()
            if email == decryptedEmail:
                users_list[decryptedEmail] = account
            account = cursor.fetchone()
        return render_template('profile(customer).html', users_list=users_list)
    return redirect(url_for('login'))


@elly.route('/deleteAcc/<email>', methods=['POST'])  # for customer
def delete_acc(email):
    if not check_role('Customer'):
        return redirect(url_for('home'))
    try:
        session.pop('email', None)
        session.pop('customer', None)
    except:
        flash('User is not logged in')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers')
    account = cursor.fetchone()
    while account is not None:
        key = account['symmetrickey']
        encrypted_email = account['encrypted_email']
        # Load the key
        f = Fernet(key)
        # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
        # using.encode()
        decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
        decryptedEmail = decryptedEmail_Binary.decode()
        if email == decryptedEmail:
            fname = account['fname']
            lname = account['lname']
            cursor.execute('DELETE FROM Customers WHERE fname = %s and lname = %s', (fname, lname))
        account = cursor.fetchone()
    mysql.connection.commit()

    return redirect(url_for('home'))


# ssp
@elly.route('/pwSecurity', methods=['GET', 'POST'])  # SSP CODE DONE BY ELLY
def pwSecurity():
    if not check_role('Customer'):
        return redirect(url_for('home'))
    msg = ''
    fname = session.get('fname')
    lname = session.get('lname')
    pwSecurity = PwSecurity(request.form)
    if 'email' in session:
        if request.method == 'POST' and pwSecurity.validate():
            security_answer = request.form['security_answer']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT hashed_security_ans FROM Customers WHERE fname = %s and lname = %s', (fname, lname))
            account = cursor.fetchone()
            answer = account['hashed_security_ans']
            if str(polynomialRollingHash(security_answer)) == str(answer):
                return redirect(url_for('elly.update_password'))
    return render_template('updatepwSecurity.html', msg='', form=pwSecurity)


@elly.route('/updatePassword', methods=['GET', 'POST'])  # SSP CODE DONE BY ELLY
def update_password():
    if not check_role('Customer'):
        return redirect(url_for('home'))
    msg = ''
    if 'email' in session:
        email = session.get('email')
        update_password = UpdatePassword(request.form)
        if request.method == 'POST' and 'passwd' in request.form:
            newpassword = request.form['passwd']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Customers')
            account = cursor.fetchone()
            while account is not None:
                key = account['symmetrickey']
                f = Fernet(key)
                decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                decryptedEmail = decryptedEmail_Binary.decode()
                if email == decryptedEmail:
                    break
            fname = account['fname']
            lname = account['lname']
            salt = bcrypt.gensalt(rounds=16)
            hash_password = bcrypt.hashpw(newpassword.encode(), salt)
            cursor.execute('UPDATE Customers SET hashed_password = %s WHERE fname = %s and lname = %s',
                           (hash_password, fname, lname))

            mysql.connection.commit()
            session['Password Updated'] = 'Password has been updated'
            return redirect(url_for('elly.profile'))
        return render_template('updatePassword(cust).html', msg='', form=update_password)


@elly.route('/updateProfile/<email>/', methods=['GET', 'POST'])
def update_profile(email):
    if not check_role('Customer'):
        return redirect(url_for('home'))
    update_profile_form = UpdateProfile(request.form)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers')
    account = cursor.fetchone()
    while account is not None:
        key = account['symmetrickey']
        # Load the key
        f = Fernet(key)
        # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
        # using.encode()
        decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
        # call .decode () to convert from Binary to String – to be displayed in Home.html.
        decryptedEmail = decryptedEmail_Binary.decode()
        if decryptedEmail == email:
            break
        else:
            account = cursor.fetchone()
    if request.method == 'POST' and update_profile_form.validate():
        # users_dict = {}
        # db = shelve.open('storage.db', 'w')
        # users_dict = db['Users']

        fname = account['fname']
        lname = account['lname']
        id = account['id']

        # user = users_dict.get(email)
        # user.set_first_name(update_profile_form.first_name.data)
        # user.set_last_name(update_profile_form.last_name.data)
        # user.set_email(update_profile_form.email.data)
        # db['Users'] = users_dict
        # db.close()

        key = Fernet.generate_key()
        f = Fernet(key)
        encryptedEmail = f.encrypt(update_profile_form.email.data.encode())

        cursor.execute(
            'UPDATE Customers SET fname = %s, lname = %s, encrypted_email = %s, symmetrickey = %s WHERE id = %s',
            (update_profile_form.first_name.data, update_profile_form.last_name.data, encryptedEmail, key, str(id)))

        mysql.connection.commit()

        return redirect(url_for('elly.profile'))
    else:

        key = account['symmetrickey']
        # Load the key
        f = Fernet(key)
        # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
        # using.encode()
        decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
        # call .decode () to convert from Binary to String – to be displayed in Home.html.
        decryptedEmail = decryptedEmail_Binary.decode()

        update_profile_form.first_name.data = account['fname']
        update_profile_form.last_name.data = account['lname']
        update_profile_form.email.data = decryptedEmail

        return render_template('updateProfile.html', form=update_profile_form)


@elly.route('/createLocation', methods=['GET', 'POST'])
def create_location():
    if not check_role('Staff'):
        return redirect(url_for('home'))
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
    if not check_role('Staff'):
        return redirect(url_for('home'))
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
    if not check_role('Staff'):
        return redirect(url_for('home'))
    locations_dict = {}
    db = shelve.open('location.db', 'w')
    locations_dict = db['Locations']

    locations_dict.pop(id)

    db['Locations'] = locations_dict
    db.close()

    return redirect(url_for('elly.retrieve_locations'))


@elly.route('/updateLocation/<int:id>/', methods=['GET', 'POST'])
def update_location(id):
    if not check_role('Staff'):
        return redirect(url_for('home'))
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
