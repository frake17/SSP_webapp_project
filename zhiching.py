import shelve

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint

import User
from Forms import CreateStaff, \
    self_collection_update, deliverymen_status_update, deliverymen_profile_update

# SSP CODE
from flask_mysqldb import MySQL
import MySQLdb.cursors
from cryptography.fernet import Fernet
import bcrypt
from url_jumping import check_role

qing = Flask(__name__)
qing.secret_key = 'any_random_string'
qing.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
qing.config["SESSION_PERMANENT"] = False

# SSP CODE
qing.config['MYSQL_HOST'] = 'localhost'
qing.config['MYSQL_USER'] = 'root'
qing.config['MYSQL_PASSWORD'] = '100carbook'
qing.config['MYSQL_DB'] = 'pythonlogin'
mysql = MySQL(qing)
qing = Blueprint('qing', __name__, template_folder='templates', static_folder='static')


@qing.route('/orders', methods=['GET', 'POST'])
def orders():
    if not check_role('Staff'):
        return redirect(url_for('home'))
    db = shelve.open('storage.db', 'r')
    try:
        collect_dict = db['confirmed_collect']
        delivery_dict = db['confirmed_delivery']
        delivery_man_dict = db['Deliverymen']
    except:
        return redirect(url_for('home'))

    collect_list = []
    delivery_list = []
    delivery_man = []
    for key in collect_dict:
        order_collect = collect_dict.get(key)
        collect_list.append(order_collect)

    for key in delivery_dict:
        order_delivery = delivery_dict.get(key)
        delivery_list.append(order_delivery)

    for key in delivery_man_dict:
        man = delivery_man_dict.get(key)
        delivery_man.append(man)
    return render_template('orders.html', collect=collect_list, deliver=delivery_list, man=delivery_man)


@qing.route('/Dest_West', methods=["POST", "GET"])
def Dest_West():
    deliverymen_dict = {}
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('smth')
    db.close()

    order_list = []
    deliverymen_list = []
    #for key in deliverymen_dict:
    #    deliverymen = deliverymen_dict.get(key)
    #    if deliverymen.get_regions() == 'W':
    #        deliverymen_list.append(deliverymen)

    #for key in order_dict:
    #    order_deliver = order_dict.get(key)
    #    if order_deliver.get_location() == 'West':
    #        order_list.append(order_deliver)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Customers WHERE ROLE = 'Deliveryman' ")
    account = cursor.fetchone()
    while account is not None:
        if account['region'] == 'West':
            deliverymen_list.append(account)

    return render_template('Dest_West.html', deliveryman_list=deliverymen_list, order_list=order_list)


@qing.route('/Dest_North')
def Dest_North():
    deliverymen_dict = {}
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('smth')
    db.close()

    order_list = []
    deliverymen_list = []
    #for key in deliverymen_dict:
    #    deliverymen = deliverymen_dict.get(key)
    #    if deliverymen.get_regions() == 'N':
    #        deliverymen_list.append(deliverymen)

    #for key in order_dict:
    #    order_deliver = order_dict.get(key)
    #    if order_deliver.get_location() == 'North':
    #        order_list.append(order_deliver)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Customers WHERE ROLE = 'Deliveryman' ")
    account = cursor.fetchone()
    while account is not None:
        if account['region'] == 'North':
            deliverymen_list.append(account)

    return render_template('Dest_North.html', deliveryman_list=deliverymen_list, order_list=order_list)


@qing.route('/Dest_South')
def Dest_South():
    order_dict = {}
    deliverymen_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('smth')
    db.close()

    order_list = []
    deliverymen_list = []
    #for key in deliverymen_dict:
    #    deliverymen = deliverymen_dict.get(key)
    #    if deliverymen.get_regions() == 'S':
    #        deliverymen_list.append(deliverymen)

    #for key in order_dict:
    #    order_deliver = order_dict.get(key)
    #    if order_deliver.get_location() == 'South':
    #        order_list.append(order_deliver)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Customers WHERE ROLE = 'Deliveryman' ")
    account = cursor.fetchone()
    while account is not None:
        if account['region'] == 'South':
            deliverymen_list.append(account)

    return render_template('Dest_South.html', deliveryman_list=deliverymen_list, order_list=order_list)


@qing.route('/Dest_East', methods=["POST", "GET"])
def Dest_East():
    deliverymen_dict = {}
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('smth')
    db.close()

    order_list = []
    deliverymen_list = []
    #for key in deliverymen_dict:
    #    deliverymen = deliverymen_dict.get(key)
    #    if deliverymen.get_regions() == 'E':
    #        deliverymen_list.append(deliverymen)

    #for key in order_dict:
    #    order_deliver = order_dict.get(key)
    #    if order_deliver.get_location() == 'East':
    #        order_list.append(order_deliver)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Customers WHERE ROLE = 'Deliveryman' ")
    account = cursor.fetchone()
    while account is not None:
        if account['region'] == 'East':
            deliverymen_list.append(account)

    return render_template('Dest_East.html', deliveryman_list=deliverymen_list, order_list=order_list)


@qing.route('/All_Deliveries')
def All_Deliveries():
    if not check_role('Staff'):
        return redirect(url_for('home'))
    order_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        order_dict = db['confirmed_delivery']
    except:
        print('not created')

    order_list = []
    for key in order_dict:
        order_deliver = order_dict.get(key)
        order_list.append(order_deliver)
    return render_template('All_Deliveries.html', order_list=order_list)


@qing.route('/All_Self_collection')
def All_Self_collection():
    if not check_role('Staff'):
        return redirect(url_for('home'))
    order_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        order_dict = db['confirmed_collect']
    except:
        print('not created')

    order_list = []
    for key in order_dict:
        order_collect = order_dict.get(key)
        order_list.append(order_collect)
    return render_template('All_Self_collection.html', order_list=order_list)


@qing.route('/Create_Deliverymen', methods=['GET', 'POST'])
def Create_Deliverymen():
    if not check_role('HR'):
        return redirect(url_for('home'))
    count = 1
    create_Staff_form = CreateStaff(request.form)
    if request.method == 'POST' and create_Staff_form.validate():
        deliverymen_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            deliverymen_dict = db["Deliverymen"]
            while count in deliverymen_dict:
                count += 1
        except:
            print("Error in retrieving Users from storage.db.")

        deliverymen = User.Deliverymen(create_Staff_form.first_name.data, create_Staff_form.last_name.data,
                                       create_Staff_form.email.data, create_Staff_form.gender.data,
                                       create_Staff_form.contact_no.data, create_Staff_form.regions.data,
                                       create_Staff_form.remarks.data)

        deliverymen_dict[deliverymen.get_Deliverymen_id()] = deliverymen
        db['Deliverymen'] = deliverymen_dict
        deliverymen_login = {}
        try:
            deliverymen_login = db["Deliverymen_login"]
        except:
            print("Error in retrieving Deliverymen from storage.db")

        deliverymen_login[create_Staff_form.email.data] = deliverymen.get_Deliverymen_id()
        db["Deliverymen_login"] = deliverymen_login
        db.close()

        # SSP CODES
        staffid = create_Staff_form.staff_id.data
        first_name = create_Staff_form.first_name.data
        last_name = create_Staff_form.last_name.data
        gender = create_Staff_form.gender.data
        email = create_Staff_form.email.data
        role = create_Staff_form.role.data
        outlet = create_Staff_form.outlet.data
        region = create_Staff_form.regions.data
        password = create_Staff_form.password.data
        phone_num = create_Staff_form.contact_no.data
        remarks = create_Staff_form.remarks.data
        status = ""

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Staff')
        account = cursor.fetchone()
        while account is not None:
            fname = account['fname']
            lname = account['lname']
            key = account['symmetrickey']
            id = account['StaffID']
            f = Fernet(key)
            decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
            decryptedEmail = decryptedEmail_Binary.decode()
            if (fname == first_name and lname == last_name) or decryptedEmail == email or staffid == id:
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

            # Symmetric Key Encryption
            # Generate a random Symmetric key. Keep this key in your database
            key = Fernet.generate_key()
            phone_num_key = Fernet.generate_key()
            # Load the key into the Crypto API
            f_phone = Fernet(phone_num_key)
            f = Fernet(key)
            # Encrypt the email and convert to bytes by calling f.encrypt()
            encryptedEmail = f.encrypt(email.encode())
            encrypted_phone = f_phone.encrypt(str(phone_num).encode())
            Staffstatus = 'enabled'

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO staff VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (staffid, first_name, last_name, gender, encryptedEmail, role, outlet, 'NULL', region,
                            hash_password, encrypted_phone, remarks, key, phone_num_key, Staffstatus))
            mysql.connection.commit()
            session['fname'] = first_name
            session['lname'] = last_name
            session['staff_email'] = email

            session['Deliverymen_created'] = deliverymen.get_first_name() + ' ' + deliverymen.get_last_name()
            return redirect(url_for('qing.Display_Staff'))
        else:
            session['registered'] = 'Name or email or ID have been registered'

    return render_template('Create_Staff.html', form=create_Staff_form)


@qing.route('/Display_Deliverymen',
            defaults={'sort': None, 'id': None})  # ?? test with have id and not sort, see what id does
@qing.route('/Display_Deliverymen/<sort>', defaults={'id': None})
@qing.route('/Display_Deliverymen/<sort>/<id>')
def Display_Staff(sort, id):
    if not check_role('HR'):
        return redirect(url_for('home'))
    users_list = {}
    order_list = {}
    decryptedEmail = 'NULL'
    db = shelve.open('storage.db', 'r')
    try:
        users_dict = db['Deliverymen']
        assign_dict = db['assignDeliverymen']
        if id is not None:
            order_list = assign_dict.get(id)

    except:
        print("Error in displaying Users from storage.db.")
        users_dict = {}
    db.close()

    # users_list = []
    # for key in users_dict:
    #    user = users_dict.get(key)
    #     users_list.append(user)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Staff")
    account = cursor.fetchone()
    while account is not None:
        if sort == 'Staff':
            if account:
                if account['role'] == 'Staff':
                    # Decrypt Email
                    # Extract the Symmetric-key from Accounts DB
                    key = account['symmetrickey']
                    # Load the key
                    f = Fernet(key)
                    # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                    # using.encode()
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    # call .decode () to convert from Binary to String – to be displayed in Home.html.
                    decryptedEmail = decryptedEmail_Binary.decode()
                    users_list[decryptedEmail] = account
        elif sort == 'Manager':
            if account:
                if account['role'] == 'Manager':
                    # Decrypt Email
                    # Extract the Symmetric-key from Accounts DB
                    key = account['symmetrickey']
                    # Load the key
                    f = Fernet(key)
                    # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                    # using.encode()
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    # call .decode () to convert from Binary to String – to be displayed in Home.html.
                    decryptedEmail = decryptedEmail_Binary.decode()
                    users_list[decryptedEmail] = account
        elif sort == 'Deliverymen':
            if account:
                if account['role'] == 'Deliverymen':
                    # Decrypt Email
                    # Extract the Symmetric-key from Accounts DB
                    key = account['symmetrickey']
                    # Load the key
                    f = Fernet(key)
                    # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                    # using.encode()
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    # call .decode () to convert from Binary to String – to be displayed in Home.html.
                    decryptedEmail = decryptedEmail_Binary.decode()
                    users_list[decryptedEmail] = account
        elif sort == 'North':
            if account:
                if account['region'] == 'North':
                    # Decrypt Email
                    # Extract the Symmetric-key from Accounts DB
                    key = account['symmetrickey']
                    # Load the key
                    f = Fernet(key)
                    # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                    # using.encode()
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    # call .decode () to convert from Binary to String – to be displayed in Home.html.
                    decryptedEmail = decryptedEmail_Binary.decode()
                    users_list[decryptedEmail] = account
        elif sort == 'South':
            if account:
                if account['region'] == 'South':
                    # Decrypt Email
                    # Extract the Symmetric-key from Accounts DB
                    key = account['symmetrickey']
                    # Load the key
                    f = Fernet(key)
                    # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                    # using.encode()
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    # call .decode () to convert from Binary to String – to be displayed in Home.html.
                    decryptedEmail = decryptedEmail_Binary.decode()
                    users_list[decryptedEmail] = account
        elif sort == 'East':
            if account:
                if account['region'] == 'East':
                    # Decrypt Email
                    # Extract the Symmetric-key from Accounts DB
                    key = account['symmetrickey']
                    # Load the key
                    f = Fernet(key)
                    # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                    # using.encode()
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    # call .decode () to convert from Binary to String – to be displayed in Home.html.
                    decryptedEmail = decryptedEmail_Binary.decode()
                    users_list[decryptedEmail] = account
        elif sort == 'West':
            if account:
                if account['region'] == 'West':
                    # Decrypt Email
                    # Extract the Symmetric-key from Accounts DB
                    key = account['symmetrickey']
                    # Load the key
                    f = Fernet(key)
                    # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                    # using.encode()
                    decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                    # call .decode () to convert from Binary to String – to be displayed in Home.html.
                    decryptedEmail = decryptedEmail_Binary.decode()
                    users_list[decryptedEmail] = account
        else:
            if account['role'] != 'HR':
                print(account)
                # Decrypt Email
                # Extract the Symmetric-key from Accounts DB
                key = account['symmetrickey']
                phone_num_key = account['phone_num_key']
                # Load the key
                f = Fernet(key)
                f_phone = Fernet(phone_num_key)
                # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                # using.encode()
                decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                decryptedPhone_Binary = f_phone.decrypt(account['phone_num'].encode())
                # call .decode () to convert from Binary to String – to be displayed in Home.html.
                decryptedEmail = decryptedEmail_Binary.decode()
                decryptedPhone = decryptedPhone_Binary.decode()
                users_list[decryptedEmail] = account
                users_list.get(decryptedEmail)['phone_num'] = decryptedPhone
            elif account['role'] == 'HR':
                key = account['symmetrickey']
                f = Fernet(key)
                decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                decryptedEmail = decryptedEmail_Binary.decode()
                users_list[decryptedEmail] = account
        account = cursor.fetchone()
    return render_template('Display_Deliverymen.html', count=len(users_list), users_list=users_list,
                           order_list=order_list)


@qing.route('/updateDeliverymen/<id>/', methods=['GET', 'POST'])
def update_Deliverymen(id):
    if not check_role('HR'):
        return redirect(url_for('home'))
    update_Deliverymen_form = deliverymen_profile_update(request.form)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Staff")
    account_list = cursor.fetchall()
    if request.method == 'POST' and update_Deliverymen_form.validate():
        for account in account_list:
            if account['StaffID'] == id:
                fname = update_Deliverymen_form.first_name.data
                lname = update_Deliverymen_form.last_name.data
                gender = update_Deliverymen_form.gender.data
                email = update_Deliverymen_form.email.data
                phone_num = update_Deliverymen_form.contact_no.data
                password = update_Deliverymen_form.password.data
                region = update_Deliverymen_form.regions.data
                remarks = update_Deliverymen_form.remarks.data
                key = account['symmetrickey']
                phone_key = account['phone_num_key']

                f = Fernet(key)
                f_phone = Fernet(phone_key)
                encryptedEmail = f.encrypt(email.encode())
                encryptedPhone = f_phone.encrypt(str(phone_num).encode())

                salt = bcrypt.gensalt(rounds=16)
                hash_password = bcrypt.hashpw(password.encode(), salt)

                if password != '' or password != ' ':
                    cursor.execute(
                        'UPDATE Staff SET fname = %s, lname = %s, gender = %s, encrypted_email = %s, phone_num = %s, region = %s, remarks = %s, hashed_password = %s WHERE StaffID = %s',
                        (
                            fname, lname, gender, encryptedEmail, encryptedPhone, region, remarks, hash_password, id
                        ))
                else:
                    cursor.execute(
                        'UPDATE Staff SET fname = %s, lname = %s, gender = %s, encrypted_email = %s, phone_num = %s, region = %s, remarks = %s, WHERE StaffID = %s',
                        (
                            fname, lname, gender, encryptedEmail, encryptedPhone, region, remarks, id
                        ))
                mysql.connection.commit()

        return redirect(url_for('qing.Display_Staff'))
    else:

        for account in account_list:
            if account['StaffID'] == id:
                key = account['symmetrickey']
                phone_key = account['phone_num_key']
                # Load the key
                f = Fernet(key)
                f_phone = Fernet(phone_key)
                # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                # using.encode()
                decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
                decryptedPhone_Binary = f_phone.decrypt(account['phone_num'].encode())
                # call .decode () to convert from Binary to String – to be displayed in Home.html.
                decryptedEmail = decryptedEmail_Binary.decode()
                decryptedPhone = decryptedPhone_Binary.decode()
                update_Deliverymen_form.first_name.data = account['fname']
                update_Deliverymen_form.last_name.data = account['lname']
                update_Deliverymen_form.gender.data = account['gender']
                update_Deliverymen_form.email.data = decryptedEmail
                update_Deliverymen_form.contact_no.data = decryptedPhone
                update_Deliverymen_form.regions.data = account['region']
                update_Deliverymen_form.remarks.data = account['remarks']

        return render_template('updateDeliverymen.html', form=update_Deliverymen_form)


@qing.route('/deleteDeliverymen/<id>', methods=['POST'])
def delete_Deliverymen(id):
    if not check_role('HR'):
        return redirect(url_for('home'))
    # SSP CODE
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Staff")
    account = cursor.fetchone()
    if account:
        if account['StaffID'] == id:
            cursor.execute('DELETE FROM Staff WHERE StaffID = %s', (id))
            mysql.connection.commit()

    return redirect(url_for('qing.Display_Staff'))


@qing.route('/deleteOrders/<int:id>/<int:deliverymen_id>', methods=['POST'])
def deleteOrders(id, deliverymen_id):
    orders_dict = {}
    db = shelve.open('storage.db', 'w')
    orders_dict = db['assignDeliverymen']
    deleteOrders = orders_dict.get(deliverymen_id)
    deleteOrders.pop(id)
    db['assignDeliverymen'] = orders_dict
    return redirect(url_for('qing.ordersAssigned', id=deliverymen_id))


@qing.route('/orders_assigned/<int:id>', methods=['POST'])
def orders_assigned(id):
    db = shelve.open('storage.db', 'c')
    assign_dict = db['assignDeliverymen']
    order_list = assign_dict.get(id)


@qing.route('/Deliveryman_North/')
def Deliveryman_North():
    deliverymen_dict = {}
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('error')
    db.close()

    order_list = []
    deliverymen_list = []
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'N':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'North':
            order_list.append(order_deliver)

    return render_template('Deliveryman_North.html', users_list=deliverymen_list, order_list=order_list,
                           count=len(deliverymen_list))


@qing.route('/Deliveryman_South/')
def Deliveryman_South():
    deliverymen_dict = {}
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('error')
    db.close()

    order_list = []
    deliverymen_list = []
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'S':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'South':
            order_list.append(order_deliver)

    return render_template('Deliveryman_South.html', users_list=deliverymen_list, order_list=order_list,
                           count=len(deliverymen_list))


@qing.route('/Deliveryman_East/')
def Deliveryman_East():
    deliverymen_dict = {}
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('error')
    db.close()

    order_list = []
    deliverymen_list = []
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'E':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'East':
            order_list.append(order_deliver)

    return render_template('Deliveryman_East.html', users_list=deliverymen_list, order_list=order_list,
                           count=len(deliverymen_list))


@qing.route('/Deliveryman_West/')
def Deliveryman_West():
    deliverymen_dict = {}
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        deliverymen_dict = db['Deliverymen']
        order_dict = db['confirmed_delivery']
    except:
        print('error')
    db.close()

    order_list = []
    deliverymen_list = []
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'W':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'West':
            order_list.append(order_deliver)

    return render_template('Deliveryman_West.html', users_list=deliverymen_list, order_list=order_list,
                           count=len(deliverymen_list))


@qing.route('/assign/<NSEW>/<int:id>/<int:orderid>', methods=["POST", "GET"])
def assign(NSEW, id, orderid):
    users_dict = {}
    order_dict = {}
    order_list = []
    db = shelve.open('storage.db', 'c')
    # users_dict = db['Deliverymen']
    order_dict = db['confirmed_delivery']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Staff WHERE role = 'Deliveryman'")
    account = cursor.fetchone()
    if account:
        if int(account['StaffID']) == id:
            assign_dict = {}
            try:
                assign_dict = db['assignDeliverymen']
                if id in assign_dict:
                    order_list = assign_dict.get(id)
            except:
                print('No database')
            current_order = order_dict.get(orderid)
            current_order.set_status('assign')
            order_list.append(current_order)
            assign_dict[account['StaffID']] = order_list
            db['assignDeliverymen'] = assign_dict
            db['confirmed_delivery'] = order_dict
            db.close()
            session['OrdersID_assigned'] = account['StaffID']
            session['Orders_assigned'] = account['fname'] + account['lname']
            if NSEW == 'North':
                return redirect(url_for('qing.Dest_North'))
            elif NSEW == 'South':
                return redirect(url_for('qing.Dest_South'))
            elif NSEW == 'East':
                return redirect(url_for('qing.Dest_East'))
            elif NSEW == 'West':
                return redirect(url_for('qing.Dest_West'))
    return redirect(url_for('qing.All_Deliveries'))


@qing.route('/updateSelfCollection/<int:id>/', methods=['GET', 'POST'])
def updateSelfCollection(id):
    updateSelfCollection_form = self_collection_update(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        print(updateSelfCollection_form.name.data, updateSelfCollection_form.status.data)
        users_dict = db['confirmed_collect']
        user = users_dict.get(id)
        updateSelfCollection_form.name.data = user.get_name()
        updateSelfCollection_form.number.data = user.get_number()
        user.set_name(updateSelfCollection_form.name.data)
        user.set_phone(updateSelfCollection_form.number.data)
        user.set_status(updateSelfCollection_form.status.data)

        db['confirmed_collect'] = users_dict
        db.close()

        return redirect(url_for('qing.All_Self_collection'))

    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['confirmed_collect']
        db.close()

        user = users_dict.get(id)
        updateSelfCollection_form.name.data = user.get_name()
        updateSelfCollection_form.number.data = user.get_number()

        return render_template('updateSelfCollection.html', form=updateSelfCollection_form)


@qing.route('/ordersAssigned/<int:id>/', methods=['GET', 'POST'])
def ordersAssigned(id):
    index = 0
    db = shelve.open('storage.db', 'r')
    assign_deliverymen = {}
    ordersAssigned_list = []
    id = str(id)
    try:
        assign_deliverymen = db['assignDeliverymen']
        if id in assign_deliverymen:
            ordersAssigned_list = assign_deliverymen.get(id)
        else:
            ordersAssigned_list = []
    except:
        print('anything')
        return redirect(url_for('qing.Display_Staff'))
    deliverymen_id = id
    print(assign_deliverymen, ordersAssigned_list)
    return render_template('ordersAssigned.html', order_list=ordersAssigned_list, count=len(ordersAssigned_list),
                           deliverymen_id=deliverymen_id, index=index)


@qing.route('/Outlet_North')
def Outlet_North():
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        order_dict = db['confirmed_collect']
    except:
        print('not created')

    order_list = []
    for key in order_dict:
        order_collected = order_dict.get(key)
        if order_collected.get_general_location() == 'North':
            order_list.append(order_collected)

    return render_template('Outlet_North.html', order_list=order_list)


@qing.route('/Outlet_South')
def Outlet_South():
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        order_dict = db['confirmed_collect']
    except:
        print('not created')
        db.close()

    order_list = []
    for key in order_dict:
        order_collected = order_dict.get(key)
        if order_collected.get_general_location() == 'South':
            order_list.append(order_collected)
    return render_template('Outlet_South.html', order_list=order_list)


@qing.route('/Outlet_East')
def Outlet_East():
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        order_dict = db['confirmed_collect']
    except:
        print('not created')
        db.close()

    order_list = []
    for key in order_dict:
        order_collected = order_dict.get(key)
        if order_collected.get_general_location() == 'East':
            order_list.append(order_collected)

    return render_template('Outlet_East.html', order_list=order_list)


@qing.route('/Outlet_West')
def Outlet_West():
    order_dict = {}
    db = shelve.open('storage.db', 'r')
    location_db = shelve.open(('location.db', 'c'))
    try:
        order_dict = db['confirmed_collect']
        location = db['Locations']
    except:
        print('not created')
        db.close()

    order_list = []
    for key in order_dict:
        order = order_dict.get(key)
        if order.get_general_location() == 'West':
            order_list.append(order)

    return render_template('Outlet_West.html', order_list=order_list)


@qing.route('/deliverymen_update_status/<int:id>/', methods=['GET', 'POST'])  # Orders
def deliverymen_update_status(id):
    deliverymen_update_status_form = deliverymen_status_update(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        print(deliverymen_update_status_form.name.data, deliverymen_update_status_form.status.data)
        users_dict = db['confirmed_delivered']
        user = users_dict.get(id)
        deliverymen_update_status_form.name.data = user.get_name()
        deliverymen_update_status_form.phone.data = user.get_phone()
        user.set_name(deliverymen_update_status_form.name.data)
        user.set_phone(deliverymen_update_status_form.phone.data)
        user.set_status(deliverymen_update_status_form.status.data)

        db['confirmed_delivered'] = users_dict
        db.close()

        return redirect(url_for('deliverymen_update_status.html', form=deliverymen_update_status_form))

    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['confirmed_collect']
        db.close()

        user = users_dict.get(id)
        print(users_dict)
        print(user.get_name(), user.get_number())
        deliverymen_update_status_form.name.data = user.get_name()
        deliverymen_update_status_form.data = user.get_phone()
        print(deliverymen_update_status_form.name.data)
        print(deliverymen_update_status_form.number.data)

        return render_template('updateSelfCollection.html', form=deliverymen_update_status_form)


@qing.route('/deliverymen_update_profile/<int:id>/',
            methods=['GET', 'POST'])  # deliverymen Only update region remarks contact number
def deliverymen_update_profile(id):
    deliverymen_update_profile_form = deliverymen_profile_update(request.form)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Staff")
    account = cursor.fetchone()
    if request.method == 'POST' and deliverymen_update_profile_form.validate():
        # users_dict = {}
        # db = shelve.open('storage.db', 'w')
        # users_dict = db['Deliverymen']

        # user = users_dict.get(id)
        # user.set_first_name(deliverymen_update_profile_form.first_name.data)
        # user.set_last_name(deliverymen_update_profile_form.last_name.data)
        # user.set_gender(deliverymen_update_profile_form.gender.data)
        # user.set_email(deliverymen_update_profile_form.email.data)
        # user.set_contact_no(deliverymen_update_profile_form.contact_no.data)
        # user.set_regions(deliverymen_update_profile_form.regions.data)
        # user.set_remarks(deliverymen_update_profile_form.remarks.data)

        # db['Deliverymen'] = users_dict
        # db.close()

        # session['Deliverymen_Profile_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        if account:
            if account['StaffID'] == id:
                fname = deliverymen_update_profile_form.first_name.data
                lname = deliverymen_update_profile_form.last_name.data
                gender = deliverymen_update_profile_form.gender.data
                email = deliverymen_update_profile_form.email.data
                phone_num = deliverymen_update_profile_form.contact_no.data
                region = deliverymen_update_profile_form.regions.data
                remarks = deliverymen_update_profile_form.remarks.data
                key = account['symmetrickey']

                f = Fernet(key)
                # Encrypt the email and convert to bytes by calling f.encrypt()
                encryptedEmail = f.encrypt(email.encode())

                cursor.execute(
                    'UPDATE Staff SET fname = %s, lname = %s, gender = %s, email = %s, phone_num = %s, region = %s, remakrs = %s WHERE StaffID = %s',
                    (
                        fname, lname, gender, encryptedEmail, phone_num, region, remarks, id
                    ))
                mysql.connection.commit()

        return redirect(url_for('qing.DeliverymenProfile'))
    else:
        # users_dict = {}
        # db = shelve.open('storage.db', 'r')
        # users_dict = db['Deliverymen']
        # db.close()

        # user = users_dict.get(id)
        # deliverymen_update_profile_form.first_name.data = user.get_first_name()
        # deliverymen_update_profile_form.last_name.data = user.get_last_name()
        # deliverymen_update_profile_form.gender.data = user.get_gender()
        # deliverymen_update_profile_form.email.data = user.get_email()
        # deliverymen_update_profile_form.contact_no.data = user.get_contact_no()
        # deliverymen_update_profile_form.regions.data = user.get_regions()
        # deliverymen_update_profile_form.remarks.data = user.get_remarks()

        if account:
            if account['StaffID'] == id:
                key = account['symmetrickey']
                # Load the key
                f = Fernet(key)
                # Call f.decrypt() to decrypt the data. Convert data from Database to bytes/binary by
                # using.encode()
                decryptedEmail_Binary = f.decrypt(account['email'].encode())
                # call .decode () to convert from Binary to String – to be displayed in Home.html.
                decryptedEmail = decryptedEmail_Binary.decode()
                deliverymen_update_profile_form.first_name.data = account['fname']
                deliverymen_update_profile_form.last_name.data = account['lname']
                deliverymen_update_profile_form.gender.data = account['gender']
                deliverymen_update_profile_form.email.data = decryptedEmail
                deliverymen_update_profile_form.contact_no.data = account['phone_num']
                deliverymen_update_profile_form.regions.data = account['region']
                deliverymen_update_profile_form.remarks.data = account['remarks']

        return render_template('deliverymen_update_profile.html', form=deliverymen_update_profile_form)


@qing.route('/deliverymen_orders')  # Delivery men see his orders
def deliverymen_orders():
    if not check_role('Deliveryman'):
        return redirect(url_for('home'))
    email = session.get('email')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    orders_list = []
    db = shelve.open('storage.db', 'r')
    assign_orders = db['assignDeliverymen']
    cursor.execute('Select * From Staff')
    account = cursor.fetchone()
    while account is not None:
        if account:
            key = account['symmetrickey']
            f = Fernet(key)
            decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
            decryptedEmail = decryptedEmail_Binary.decode()
            if decryptedEmail == email:
                orders_list = assign_orders.get(account['StaffID'])
        account = cursor.fetchone()
    return render_template('ordersAssigned(deliveryman).html', orders_list=orders_list)


@qing.route('/DeliverymenProfile', methods=['GET', 'POST'])
def DeliverymenProfile():
    email = session.get('email')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Deliverymen_list = []
    cursor.execute('Select * From Staff Where role = "Deliveryman"')
    account = cursor.fetchone()
    if account:
        key = account['symmetrickey']
        f = Fernet(key)
        decryptedEmail_Binary = f.decrypt(account['encrypted_email'].encode())
        decryptedEmail = decryptedEmail_Binary.decode()
        if decryptedEmail == email:
            Deliverymen_list.append(account)
    return render_template('DeliverymenProfile.html', users_list=Deliverymen_list, email=email)


@qing.route('/disable/<int:id>/',methods=['POST'])  # SSP CODE DONE BY ZHICHING
def disable(id):
    staffStatus = session.get('staffStatus')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Staff")

    account = cursor.fetchone()
    while account is not None:
        if account['staffStatus'] == "disabled":
            cursor.execute(
                'UPDATE Staff SET staffStatus = %s WHERE StaffID = %s',
                (
                    'enabled', id
                ))
            mysql.connection.commit()
            print(account['staffStatus'])

            return redirect(url_for('qing.Display_Staff'))


        else:
            if account['staffStatus'] == 'enabled':
                cursor.execute(
                    'UPDATE Staff SET staffStatus = %s WHERE StaffID = %s',
                    (
                        "disabled", id
                    ))
                mysql.connection.commit()
                print(account['staffStatus'])

                return redirect(url_for('qing.Display_Staff'))
        account = cursor.fetchone()

    return redirect(url_for('qing.Display_Staff'))


@qing.route('/loginActivity(Staff)', methods=['POST','GET']) # SSP CODE DONE BY ZHICHING
def loginActivity():
    users_list = []
    fname = session.get('fname')
    lname = session.get('lname')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM StaffLoginActivity WHERE fname = %s and lname = %s", (fname, lname))
    account = cursor.fetchone()
    while account is not None:
        users_list.append(account)
        account = cursor.fetchone()
    print(users_list)
    return render_template('loginActivity(cust).html',users_list = users_list)
