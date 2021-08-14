import os
import shelve
from datetime import timedelta, datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, current_app

import item
from Forms import Item, Order, self_collect, Supplier, self_collection_update
from flask_mysqldb import MySQL
import MySQLdb.cursors
from cryptography.fernet import Fernet
from url_jumping import check_role

UPLOAD_FOLDER = '/static/img/uploaded'
ALLOWED_EXTENSIONS = {'png'}

kin = Flask(__name__)
kin.secret_key = 'any_random_string'
kin.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
kin.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
kin.config["SESSION_PERMANENT"] = False

kin.config['MYSQL_HOST'] = 'localhost'
kin.config['MYSQL_USER'] = 'root'
kin.config['MYSQL_PASSWORD'] = '100carbook'
kin.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(kin)

kin = Blueprint('kin', __name__, template_folder='templates', static_folder='static')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@kin.route('/stock', defaults={'sort': None}, methods=['GET', 'POST'])
@kin.route('/stock/<sort>', methods=['GET', 'POST'])
def stock(sort):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    item_dict = {}
    low_on_stock = []
    percentage = 20
    db = shelve.open('storage.db', 'c')
    try:
        item_dict = db['item']
        percentage = db['percentage']
    except:
        print("Error in retrieving Users from storage.db.")

    if request.method == 'POST':
        percentage = int(request.form['percentage'])
        db['percentage'] = percentage

    item_list = []
    for key in item_dict:
        items = item_dict.get(key)
        item_list.append(items)
        if items.get_percentage() <= percentage:
            low_on_stock.append(items)
    if sort == 'alphabet':
        item_list.sort(key=lambda x: x.get_stock_name())
    elif sort == 'LTH':
        item_list.sort(key=lambda x: x.get_stock_left())
    elif sort == 'HTL':
        item_list.sort(key=lambda x: x.get_stock_left(), reverse=True)
    db['low_stock_list'] = low_on_stock

    db.close()
    return render_template('stock.html', item_list=item_list, percentage=percentage, low_on_stock=low_on_stock,
                           count=len(low_on_stock))


@kin.route('/shop_admin', defaults={'sort': None})
@kin.route('/shop_admin/<sort>')
def shop(sort):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    items_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        items_dict = db['item']
        db.close()
    except:
        print("Error in retrieving Users from storage.db.")

    item_list = []
    for key in items_dict:
        items = items_dict.get(key)
        item_list.append(items)
    if sort == 'alphabet':
        item_list.sort(key=lambda x: x.get_stock_name())
    elif sort == 'Low_to_high_price':
        item_list.sort(key=lambda x: x.get_base_price())
    elif sort == 'High_to_low_price':
        item_list.sort(key=lambda x: x.get_base_price(), reverse=True)
    elif sort == 'brand_AtoZ':
        item_list.sort(key=lambda x: x.get_brand())
    elif sort == 'brand_ZtoA':
        item_list.sort(key=lambda x: x.get_brand(), reverse=True)
    return render_template('shop_admin.html', item_list=item_list)


@kin.route('/shop_cus', defaults={'sort': None})
@kin.route('/shop_cus/<sort>')
def shop_cus(sort):
    if not check_role('Customer'):
        return redirect(url_for('home'))
    items_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        items_dict = db['item']
        db.close()
    except:
        print("Error in retrieving Users from storage.db.")

    item_list = []
    for key in items_dict:
        items = items_dict.get(key)
        item_list.append(items)

    if sort == 'alphabet':
        item_list.sort(key=lambda x: x.get_stock_name())
    elif sort == 'Low_to_high_price':
        item_list.sort(key=lambda x: x.get_base_price())
    elif sort == 'High_to_low_price':
        item_list.sort(key=lambda x: x.get_base_price(), reverse=True)
    elif sort == 'brand_AtoZ':
        item_list.sort(key=lambda x: x.get_brand())
    elif sort == 'brand_ZtoA':
        item_list.sort(key=lambda x: x.get_brand(), reverse=True)
    return render_template('shop_cus.html', item_list=item_list)


@kin.route('/shop_display/<int:id>')
def display(id):
    db = shelve.open('storage.db', 'r')
    item_dict = db['item']
    current_item = item_dict.get(id)
    db.close()
    return render_template('shop_item_display.html', item=current_item)


@kin.route('/cart/<int:product_id>', methods=['POST', 'GET'])  # done with {user:{id:item}}
def add_to_cart(product_id):
    cart_dict = {}
    email_cart_dict = {}
    db = shelve.open('storage.db', 'c')
    try:
        email = session.get('email')
    except:
        print('no email in session')
        return url_for('login')

    try:
        email_cart_dict = db['Cart']
        if email in email_cart_dict:
            cart_dict = email_cart_dict.get(email)
    except:
        print('das')

    shop_dict = db['item']

    item_list = []  # get object of stocks
    for key in shop_dict:
        user = shop_dict.get(key)
        item_list.append(user)

    for item in item_list:  # adding to cart
        id = item.get_id()
        if product_id in cart_dict:
            item_cart = cart_dict.get(product_id)
            if item.get_stock_left() >= (item_cart.get_amount() + 1):
                print('***', item.get_stock_left(), item.get_stock_name())
                item_cart.add_amount()
                session['cart_added'] = item_cart.get_stock_name()
                break
            else:
                session['not_enough'] = item_cart.get_stock_name()
        else:
            if id == product_id:
                if item.get_stock_left() >= 1:
                    item.add_amount()
                    cart_dict[item.get_id()] = item
                    session['cart_added'] = item.get_stock_name()
                    break
                else:
                    session['not_enough'] = item.get_stock_name()

    email_cart_dict[email] = cart_dict
    db['Cart'] = email_cart_dict
    db.close()

    return redirect(url_for('kin.shop_cus'))


@kin.route('/add/<int:product_id>')
def add_cart_item(product_id):
    cart_dict = {}
    email_cart_dict = {}
    item_dict = {}
    db = shelve.open('storage.db', 'c')
    email = session.get('email')

    try:
        email_cart_dict = db['Cart']
        item_dict = db['item']
        if email in email_cart_dict:
            cart_dict = email_cart_dict.get(email)
    except:
        print('das')

    stock_item = item_dict.get(product_id)
    item = cart_dict.get(product_id)
    if stock_item.get_stock_left() > item.get_amount():
        item.add_amount()
    else:
        session['not_enough'] = item.get_stock_name()
        print('not enough stock')
    email_cart_dict[email] = cart_dict
    db['Cart'] = email_cart_dict
    db.close()

    return redirect(url_for('kin.cart'))


@kin.route('/minus/<int:product_id>')
def minus_cart_item(product_id):
    cart_dict = {}
    email_cart_dict = {}
    db = shelve.open('storage.db', 'c')
    email = session.get('email')

    try:
        email_cart_dict = db['Cart']
        if email in email_cart_dict:
            cart_dict = email_cart_dict.get(email)
    except:
        print('das')

    item = cart_dict.get(product_id)
    if item.get_amount() > 0:
        item.minus()

    if item.get_amount() == 0:
        cart_dict.pop(product_id)

    email_cart_dict[email] = cart_dict
    db['Cart'] = email_cart_dict
    db.close()

    return redirect(url_for('kin.cart'))


@kin.route('/cart')
def cart():
    cart_list = {}
    email_cart_dict = {}
    db = shelve.open('storage.db', 'c')
    item_list = []
    total = 0
    try:
        email = session.get('email')
        email_cart_dict = db['Cart']
        cart_list = email_cart_dict.get(email)
        for key in cart_list:
            user = cart_list.get(key)
            price = user.get_total()
            total += int(price)
            item_list.append(user)
    except:
        print('error')
        session['empty_cart'] = 'cart is empty'
        return redirect(url_for('kin.shop_cus'))
    session['Total_price'] = total

    return render_template('cart.html', item_list=item_list, price=total)


@kin.route('/clear_cart')
def clear_cart():
    email = session.get('email')
    db = shelve.open('storage.db', 'c')
    try:
        email_cart_dict = db['Cart']
        email_cart_dict[email] = {}
        db['Cart'] = email_cart_dict
    except:
        print('email not in dict')

    return redirect(url_for('kin.shop_cus'))


@kin.route('/delivery', methods=['POST', 'GET'])
def delivery_date():
    total = session.get('Total_price', None)
    date_now = datetime.now()
    max_date = date_now + timedelta(60)
    if total > 100:
        total = total
    else:
        total = total + 3
    if request.method == 'POST':
        date = request.form['date']
        input_date = datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
        if input_date > max_date:
            session['invalid_date'] = date + ' is invalid. Please choose another date'
            redirect(url_for('kin.delivery_date'))
        elif input_date < date_now:
            session['invalid_date'] = date + ' is invalid. Please choose another date'
            redirect(url_for('kin.delivery_date'))
        else:
            session['date'] = date
            return redirect(url_for('kin.delivery_order_details'))
    session['Total_price'] = total
    return render_template('delivery_date.html', total=total)


@kin.route('/self-collect', methods=['POST', 'GET'])
def collect_date_location():
    total = session.get('Total_price', None)
    db = shelve.open('location.db', 'c')
    locations_dict = db['Locations']
    locations_list = []
    for key in locations_dict:
        location = locations_dict.get(key)
        locations_list.append(location)
    date_now = datetime.now()
    max_date = date_now + timedelta(30)
    date_now_hour = date_now.hour

    if request.method == 'POST':
        date = request.form['date']
        input_date = datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
        time = request.form['time']
        input_hour = time[0]
        print(input_date, max_date)
        if input_date > max_date:
            session['invalid_date'] = date + ' is invalid. Please choose another date'
            redirect(url_for('kin.collect_date_location'))
        elif input_date == date_now:
            if input_hour <= date_now.hour:
                session['invalid_time'] = input_hour + ' is invalid. Please choose another timing'
                redirect(url_for('kin.collect_date_location'))
        elif input_date < date_now:
            session['invalid_date'] = date + ' is invalid. Please choose another date'
            redirect(url_for('kin.collect_date_location'))
        else:
            location = request.form['location']
            session['date'] = date
            session['time'] = time
            session['location'] = location
            return redirect(url_for('kin.self_collect_order_details'))
    session['Total_price'] = total
    return render_template('self_collect_details.html', total=total, stores=locations_list)


@kin.route('/order', methods=['GET', 'POST']) # To test
def delivery_order_details():
    if not check_role('Customer'):
        return redirect(url_for('home'))
    count = 1
    date = session.get('date', None)
    create_order = Order(request.form)
    fname = session.get('fname', None)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * From Staff Where fname = %s', fname)
    account = cursor.fetchone()
    if account:
        if account['Phone_num'] != 'NULL':
            key = account['Phone_num_key']
            f = Fernet(key)
            decrypted_phone_Binary = f.decrypt(account['Phone_num'].encode())
            decrypted_phone = decrypted_phone_Binary.decode()
            create_order.number.data = decrypted_phone
        if account['card_num'] != 'NULL':
            key = account['card_num_key']
            f = Fernet(key)
            decrypted_card_num_Binary = f.decrypt(account['card_num'].encode())
            decrypted_card_num = decrypted_card_num_Binary.decode()
            create_order.card_number.date = decrypted_card_num
        if account['card_exp_date'] != 'NULL':
            key = account['card_exp_date_key']
            f = Fernet(key)
            decrypted_card_exp_Binary = f.decrypt(account['card_exp_date'].encode())
            decrypted_card_exp = decrypted_card_exp_Binary.decode()
            create_order.exp_date.data = decrypted_card_exp
        if account['card_cvv'] != 'NULL':
            key = account['card_cvv_key']
            f = Fernet(key)
            decrypted_card_cvv_Binary = f.decrypt(account['card_cvv'].encode())
            decrypted_card_cvv = decrypted_card_cvv_Binary.decode()
            create_order.cvv.data = decrypted_card_cvv
    if request.method == 'POST' and create_order.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            users_dict = db['orders_delivery']
            while count in users_dict:
                count += 1
        except:
            print('Error in retrieving users from db')

        order_item = item.Order_delivery(create_order.name.data, create_order.number.data, create_order.postal.data,
                                         create_order.address.data, create_order.level.data,
                                         create_order.door_number.data, create_order.card_number.data,
                                         create_order.exp_date.data, create_order.cvv.data, create_order.card_type.data,
                                         create_order.general_location.data, create_order.remarks.data)
        order_item.set_card(create_order.card_type.data)
        order_item.set_id(count)  # To set new Id
        order_item.set_date(date)
        session['current_id_delivery'] = count
        users_dict[order_item.get_id()] = order_item
        db['orders_delivery'] = users_dict
        db.close()

        return redirect(url_for('kin.delivery_summary'))
    return render_template('order_details_delivery.html', form=create_order)


@kin.route('/order_self', methods=['POST', 'GET']) # To Test
def self_collect_order_details():
    if not check_role('Customer'):
        return redirect(url_for('home'))
    count = 1
    create_order_self = self_collect(request.form)
    date = session.get('date', None)
    location = session.get('location', None)
    time = session.get('time', None)
    fname = session.get('fname', None)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * From Staff Where fname = %s', fname)
    account = cursor.fetchone()
    if account:
        if account['Phone_num'] != 'NULL':
            key = account['Phone_num_key']
            f = Fernet(key)
            decrypted_phone_Binary = f.decrypt(account['Phone_num'].encode())
            decrypted_phone = decrypted_phone_Binary.decode()
            create_order_self.number.data = decrypted_phone
        if account['card_num'] != 'NULL':
            key = account['card_num_key']
            f = Fernet(key)
            decrypted_card_num_Binary = f.decrypt(account['card_num'].encode())
            decrypted_card_num = decrypted_card_num_Binary.decode()
            create_order_self.card_number.date = decrypted_card_num
        if account['card_exp_date'] != 'NULL':
            key = account['card_exp_date_key']
            f = Fernet(key)
            decrypted_card_exp_Binary = f.decrypt(account['card_exp_date'].encode())
            decrypted_card_exp = decrypted_card_exp_Binary.decode()
            create_order_self.exp_date.data = decrypted_card_exp
        if account['card_cvv'] != 'NULL':
            key = account['card_cvv_key']
            f = Fernet(key)
            decrypted_card_cvv_Binary = f.decrypt(account['card_cvv'].encode())
            decrypted_card_cvv = decrypted_card_cvv_Binary.decode()
            create_order_self.cvv.data = decrypted_card_cvv
    if request.method == 'POST' and create_order_self.validate():
        users_dict = {}
        location_dict = {}
        db_location = shelve.open('location.db', 'c')
        db = shelve.open('storage.db', 'c')
        try:
            users_dict = db['orders_self']
            location_dict = db_location['Locations']
            while count in users_dict:
                count += 1
        except:
            print('error')
        order_item = item.Order_self(create_order_self.name.data, create_order_self.number.data,
                                     create_order_self.card_number.data,
                                     create_order_self.exp_date.data, create_order_self.cvv.data,
                                     create_order_self.card_type.data)
        order_item.set_date(date)
        order_item.set_location(location)
        for key in location_dict:
            location_loop = location_dict.get(key)
            if location_loop.get_neighbourhood() + ', ' + location_loop.get_address() == location:
                general_location = location_loop.get_area()
                order_item.set_general_location(general_location)
        order_item.set_time(time)
        order_item.set_id(count)
        session['current_id_self'] = count
        users_dict[order_item.get_id()] = order_item
        db['orders_self'] = users_dict
        db.close()

        return redirect(url_for('kin.self_collect_summary'))

    return render_template('order_details_collect.html', form=create_order_self)


@kin.route('/summary')
def delivery_summary():
    if not check_role('Customer'):
        return redirect(url_for('home'))
    email = session.get('email')
    total = session.get('Total_price')
    item_list = []  # for displaying in html

    db = shelve.open('storage.db', 'c')
    order_list = db['orders_delivery']
    item_dict = db['item']
    email_cart_dict = db['Cart']
    cart_dict = email_cart_dict.get(email)

    for key in order_list:  # for displaying in html
        user = order_list.get(key)
        item_list.append(user)

    current_id = session.get('current_id_delivery')
    current = order_list.get(current_id)
    current.set_item(cart_dict)

    db['item'] = item_dict
    db.close()

    return render_template('Order_delivery_confirmation.html', item_list=item_list, current=current, total=total)


@kin.route('/summary_self')
def self_collect_summary():
    if not check_role('Customer'):
        return redirect(url_for('home'))
    email = session.get('email')
    total = session.get('Total_price')
    item_list = []  # for displaying in html (delete once intergrate with qing)

    db = shelve.open('storage.db', 'c')
    order_list = db['orders_self']
    item_dict = db['item']
    email_cart_dict = db['Cart']
    cart_dict = email_cart_dict.get(email)

    for key in order_list:  # for displaying in html (delete once intergrate with qing)
        user = order_list.get(key)
        item_list.append(user)

    current_id = session.get('current_id_self', None)
    current = order_list.get(current_id)
    current.set_item(cart_dict)

    db['item'] = item_dict
    db.close()

    return render_template('Order_collect_confirmation.html', item_list=item_list, current=current, total=total)


@kin.route('/summary_restock')
def restock_summary():
    order_list = {}
    clear_dict = {}
    item_dict = {}
    item_list = []
    db = shelve.open('storage.db', 'c')
    order_list = db['restock']
    db['Cart'] = clear_dict
    item_dict = db['item']

    for key in order_list:
        user = order_list.get(key)
        item_list.append(user)

    for key in item_dict:
        item = item_dict.get(key)
        item.set_amount_empty()
    db['item'] = item_dict

    current_id = session.get('current_id_restock', None)
    current = order_list.get(current_id)

    return render_template('restock_summary.html', item_list=item_list, current=current)


@kin.route('/Delete_order/<delivery_collect>/<int:id>')
def delete_order(delivery_collect, id):
    db = shelve.open('storage.db', 'c')
    if delivery_collect == 'delivery':
        order_dict = db['orders_delivery']
        order_dict.pop(id)
        db['orders_delivery'] = order_dict
    else:
        order_dict = db['orders_self']
        order_dict.pop(id)
        db['orders_self'] = order_dict
    db.close()
    return redirect(url_for('kin.shop_cus'))


@kin.route('/sent_order/<delivery_collect>/<int:id>')
def sent_order(delivery_collect, id):
    email = session.get('email')
    db = shelve.open('storage.db', 'c')
    email_cart_dict = db['Cart']
    item_dict = db['item']
    cart_dict = email_cart_dict.get(email)
    order_item = {}
    confirmed_delivery = {}
    confirmed_collect = {}
    try:
        confirmed_delivery = db['confirmed_delivery']
        confirmed_collect = db['confirmed_collect']
    except:
        print('No confirmed orders yet')
    for key in cart_dict:
        item = cart_dict.get(key)
        order_item[item.get_stock_name()] = item.get_amount()

    if delivery_collect == 'delivery':
        orders_delivery = db['orders_delivery']
        current_order = orders_delivery.get(id)
        current_order.set_item(order_item)
        confirmed_delivery[id] = current_order
        db['confirmed_delivery'] = confirmed_delivery
        db['orders_delivery'] = orders_delivery
    else:
        orders_collect = db['orders_self']
        current_order = orders_collect.get(id)
        current_order.set_item(order_item)
        confirmed_collect[id] = current_order
        db['confirmed_collect'] = confirmed_collect
        db['orders_self'] = orders_collect

    for key in cart_dict:
        item = cart_dict.get(key)
        for i in range(item.get_amount()):
            item.decrease_stock()
        item.set_amount_empty()
        item_dict[item.get_id()] = item

    email_cart_dict.pop(email)
    db['Cart'] = email_cart_dict
    db['item'] = item_dict
    db.close()
    return redirect(url_for('kin.shop_cus'))


@kin.route('/edit_delivery_order/<int:id>/<RSD>', methods=['POST', 'GET'])
def edit_order(id ,RSD):
    db = shelve.open('storage.db', 'c')
    update_order = Order(request.form)
    order_dict = {}
    if request.method == 'POST' and update_order.validate():
        order_dict = db['orders_delivery']

        current_order = order_dict.get(id)
        current_order.set_name(update_order.name.data)
        current_order.set_phone(update_order.number.data)
        current_order.set_postal(update_order.postal.data)
        current_order.set_address(update_order.address.data)
        current_order.set_level(update_order.level.data)
        current_order.set_door_no(update_order.door_number.data)
        current_order.set_card(update_order.card_type.data)
        current_order.set_exp(update_order.exp_date.data)
        current_order.set_ccv(update_order.cvv.data)
        current_order.set_card_no(update_order.card_number.data)
        current_order.set_location(update_order.general_location.data)
        current_order.set_remark(update_order.remarks.data)

        db['orders_delivery'] = order_dict
        db.close()
        if RSD == 'S':
            return redirect(url_for('kin.self_collect_summary'))
        elif RSD == 'D':
            return redirect(url_for('kin.delivery_summary'))
        elif RSD == 'R':
            return redirect(url_for('kin.restock_summary'))

    else:
        order_dict = db['orders_delivery']

        current_order = order_dict.get(id)
        update_order.name.data = current_order.get_name()
        update_order.number.data = current_order.get_phone()
        update_order.postal.data = current_order.get_postal()
        update_order.address.data = current_order.get_address()
        update_order.level.data = current_order.get_level()
        update_order.door_number.data = current_order.get_door()
        update_order.card_type.data = current_order.get_card()
        update_order.exp_date.data = current_order.get_exp_date()
        update_order.cvv.data = current_order.get_cvv()
        update_order.card_number.data = current_order.get_card_no()
        update_order.general_location.data = current_order.get_location()
        update_order.remarks.data = current_order.get_remark()
        return render_template('order_details_delivery.html', form=update_order)


@kin.route('/edit_collect_order/<int:id>', methods=['POST', 'GET'])
def edit_collect_order(id):
    db = shelve.open('storage.db', 'c')
    update_order = self_collect(request.form)
    if request.method == 'POST' and update_order.validate():
        order_dict = db['orders_self']

        current_order = order_dict.get(id)
        current_order.set_name(update_order.name.data)
        current_order.set_phone(update_order.number.data)
        current_order.set_card_no(update_order.card_number.data)
        current_order.set_date(update_order.exp_date.data)
        current_order.set_ccv(update_order.cvv.data)
        current_order.set_card(update_order.card_type.data)

        db['orders_self'] = order_dict
        db.close()
        return redirect(url_for('kin.self_collect_summary'))
    else:
        order_dict = db['orders_self']

        current_order = order_dict.get(id)
        update_order.name.data = current_order.get_name()
        update_order.number.data = current_order.get_number()
        update_order.card_number.data = current_order.get_card_no()
        update_order.exp_date.data = current_order.get_exp()
        update_order.cvv.data = current_order.get_cvv()
        update_order.card_type.data = current_order.get_card()

    return render_template('order_details_collect.html', form=update_order)


@kin.route('/create_item/<shop_or_stock>', methods=['GET', 'POST'])
def create_item(shop_or_stock):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    count = 1
    create_item_form = Item(request.form)
    print(create_item_form.errors)
    if request.method == 'POST' and create_item_form.validate():
        file = request.files['file']
        if file and allowed_file(file.filename):
            users_dict = {}
            db = shelve.open('storage.db', 'c')
            try:
                users_dict = db['item']
                while count in users_dict:
                    count += 1
            except:
                print('Error in retrieving users from db')
            print('worked')

            stock_item = item.Stock_item(create_item_form.stock_name.data,
                                         create_item_form.price.data, create_item_form.origin.data,
                                         create_item_form.weight.data, create_item_form.Dietary.data,
                                         create_item_form.ingredients.data, create_item_form.description.data,
                                         create_item_form.amt_of_stock.data, create_item_form.category.data,
                                         create_item_form.brand.data, create_item_form.unit.data,
                                         create_item_form.stock_unit.data)
            stock_item.set_per_box(create_item_form.subcategory_boxes.data)
            filename = create_item_form.stock_name.data + '.png'
            if filename in current_app.config['UPLOAD_FOLDER']:
                flash('similar stock is already created')
                return redirect(url_for('create_stock'))
            print(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            stock_item.set_id(count)
            users_dict[stock_item.get_id()] = stock_item
            db['item'] = users_dict
            db.close()

            session['item_created'] = stock_item.get_stock_name()

            if shop_or_stock == 'stock':
                return redirect(url_for('kin.stock',
                                        filename=filename))
            else:
                return redirect(url_for('kin.shop',
                                        filename=filename))
        else:
            print('invalid file extension')
            flash('Invalid file extension')
    return render_template('create_item.html', form=create_item_form, shop_or_stock=shop_or_stock)


@kin.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    update_item_form = Item(request.form)
    if request.method == 'POST' and update_item_form.validate():
        item_dict = {}
        db = shelve.open('storage.db', 'w')
        item_dict = db['item']
        item = item_dict.get(id)

        item.set_stock_name(update_item_form.stock_name.data)
        item.set_base_price(update_item_form.price.data)
        item.set_origin(update_item_form.origin.data)
        item.set_weight(update_item_form.weight.data)
        item.set_dietary(update_item_form.Dietary.data)
        item.set_amt_of_stock(update_item_form.amt_of_stock.data)
        item.set_cat(update_item_form.category.data)
        item.set_ingredients(update_item_form.ingredients.data)
        item.set_description(update_item_form.description.data)
        item.set_brand(update_item_form.brand.data)
        item.set_stock_unit(update_item_form.stock_unit.data)
        file = request.files['file']
        if file.filename != '':
            filename = update_item_form.stock_name.data + '.png'
            file_path = UPLOAD_FOLDER + '/' + filename
            os.remove(file_path)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        db['item'] = item_dict
        db.close()

        session['item_updated'] = item.get_stock_name()

        return redirect(url_for('kin.stock'))
    else:
        item_dict = {}
        db = shelve.open('storage.db', 'r')
        item_dict = db['item']
        db.close()

        item = item_dict.get(id)
        update_item_form.stock_name.data = item.get_stock_name()
        update_item_form.price.data = item.get_base_price()
        update_item_form.origin.data = item.get_origin()
        update_item_form.weight.data = item.get_weight()
        update_item_form.Dietary.data = item.get_dietary()
        update_item_form.category.data = item.get_category()
        update_item_form.amt_of_stock.data = item.get_amt_of_stock()
        update_item_form.ingredients.data = item.get_ingredients()
        update_item_form.description.data = item.get_description()
        update_item_form.brand.data = item.get_brand()
        update_item_form.stock_unit.data = item.get_stock_unit()

        return render_template('update_item.html', form=update_item_form)


@kin.route('/delete_stock/<int:id>', methods=['GET', 'POST'])
def delete_stock(id):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        item_dict = {}
        db = shelve.open('storage.db', 'w')
        item_dict = db['item']

        item = item_dict.get(id)
        filename = item.get_stock_name() + '.png'
        filepath = UPLOAD_FOLDER + '/' + filename
        os.remove(filepath)

        item = item_dict.pop(id)

        db['item'] = item_dict
        db.close()

        session['item_deleted'] = item.get_stock_name()

    return redirect(url_for('kin.stock'))


@kin.route('/restock/<int:id>', methods=['GET', 'POST'])
def restock(id):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    count = 0
    supplier_dict = {}
    supplier_list = []
    stock_dict = {}
    db = shelve.open('storage.db', 'c')
    stock_dict = db['item']
    current_item = stock_dict.get(id)

    try:
        supplier_dict = db['supplier']
    except:
        print('supplier not created')
    for key in supplier_dict:
        item = supplier_dict.get(key)
        supplier_for = item.get_stock()
        supplier_name = item.get_name()
        if supplier_for == current_item.get_stock_name():
            supplier_list.append(item)
            if supplier_name == current_item.get_default_suppliers():
                supplier_index = supplier_list.index(item)
                supplier_list.insert(0, supplier_list.pop(supplier_index))
    if request.method == 'POST':
        supplier = request.form['supplier']
        amount = request.form['amount']
        session['restock_order'] = supplier

        for key in stock_dict:
            stock_item = stock_dict.get(key)
            stock_id = stock_item.get_id()
            if id == stock_id:
                stock_item.increase_stock(amount)
        db['item'] = stock_dict
        db.close()
        return redirect(url_for('kin.stock'))
    return render_template('restock.html', id=id, supplier_list=supplier_list,
                           length=len(supplier_list))


@kin.route('/low_stock_bulk_restock', methods=['GET', 'POST'])
def low_stock_bulk_restock():
    db = shelve.open('storage.db', 'c')
    low_stock_list = db['low_stock_list']
    item_dict = db['item']
    quantity = request.form['quantity']

    for item in low_stock_list:
        item_id = item.get_id()
        item_in_dict = item_dict.get(item_id)
        if item_in_dict.get_default_suppliers() != '':
            item_in_dict.increase_stock(quantity)
        else:
            print(1)
            flash(item_in_dict.get_stock_name() + ' has no default supplier')
    db['item'] = item_dict
    db.close()
    return redirect(url_for('kin.stock'))


@kin.route('/delete_shop/<int:id>', methods=['GET', 'POST'])
def delete_shop(id):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        item_dict = {}
        db = shelve.open('storage.db', 'w')
        item_dict = db['item']

        item_dict.pop(id)

        db['item'] = item_dict
        db.close()

    return redirect(url_for('kin.shop'))


@kin.route('/create_supplier/<int:id>', methods=['GET', 'POST'])
def supplier(id):
    count = 1
    create_supplier = Supplier(request.form)
    if request.method == 'POST' and create_supplier.validate():
        supplier_dict = {}
        item_dict = {}
        db = shelve.open('storage.db', 'c')
        item_dict = db['item']

        try:
            supplier_dict = db['supplier']
            while count in supplier_dict:
                count += 1
        except:
            print('error')

        supplier_item = item.Supplier(create_supplier.name.data, create_supplier.email.data,
                                      create_supplier.number.data,
                                      create_supplier.location.data)
        supplier_item.set_id(count)
        stock_item = item_dict.get(id)
        supplier_item.set_stock(stock_item.get_stock_name())
        supplier_dict[supplier_item.get_id()] = supplier_item
        db['supplier'] = supplier_dict
        db.close()
        return redirect(url_for('kin.stock'))
    return render_template('create_supplier.html', form=create_supplier)


@kin.route('/suppliers', defaults={'sort': None})
@kin.route('/suppliers/<sort>')
def suppliers_list(sort):
    supplier_dict = {}
    item_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        supplier_dict = db['supplier']
    except:
        session['No_restock_obj'] = 'No restock company are created'
    db.close()

    supplier_list = []
    for key in supplier_dict:
        supplier_details = supplier_dict.get(key)
        supplier_list.append(supplier_details)

    if sort == 'Supplier_AZ':
        supplier_list.sort(key=lambda x: x.get_name())
    elif sort == 'Supplier_ZA':
        supplier_list.sort(key=lambda x: x.get_name(), reverse=True)
    elif sort == 'For_AZ':
        supplier_list.sort(key=lambda s: s.get_stock())
    elif sort == 'For_ZA':
        supplier_list.sort(key=lambda s: s.get_stock(), reverse=True)

    return render_template('suppliers.html', count=len(supplier_list), supplier_list=supplier_list)


@kin.route('/deleteSupplier/<int:id>', methods=['POST'])
def delete_supplier(id):
    if not check_role('Staff'):
        return redirect(url_for('home'))
    supplier_dict = {}
    db = shelve.open('storage.db', 'w')
    supplier_dict = db['supplier']

    supplier = supplier_dict.pop(id)

    db['supplier'] = supplier_dict
    db.close()

    session['deleted_supplier'] = supplier.get_name()
    return redirect(url_for('kin.stock'))


@kin.route('/updateSupplier/<int:id>', methods=['POST', 'GET'])
def update_supplier(id):
    update_supplier = Supplier(request.form)
    if request.method == 'POST' and update_supplier.validate():
        supplier_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            supplier_dict = db['supplier']
        except:
            print('error')

        supplier_item = supplier_dict.get(id)

        supplier_item.set_name(update_supplier.name.data)
        supplier_item.set_number(update_supplier.number.data)
        supplier_item.set_email(update_supplier.email.data)
        supplier_item.set_location(update_supplier.location.data)

        db['supplier'] = supplier_dict
        db.close()

        session['updated_supplier'] = supplier_item.get_name()

        return redirect(url_for('kin.suppliers_list'))
    else:
        supplier_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            supplier_dict = db['supplier']
        except:
            print('error')

        supplier_item = supplier_dict.get(id)

        update_supplier.name.data = supplier_item.get_name()
        update_supplier.number.data = supplier_item.get_phone()
        update_supplier.email.data = supplier_item.get_email()
        update_supplier.location.data = supplier_item.get_location()

        return render_template('update_supplier.html', form=update_supplier)


@kin.route('/set_as_default/<int:supplier_id>')
def set_default(supplier_id):
    db = shelve.open('storage.db', 'c')
    supplier_dict = db['supplier']
    stock_dict = db['item']

    current_supplier = supplier_dict.get(supplier_id)
    for_stock = current_supplier.get_stock()

    for key in stock_dict:
        current_item = stock_dict.get(key)
        if current_item.get_stock_name() == for_stock:
            current_item.set_default_supplier(current_supplier.get_name())

    db['item'] = stock_dict
    db.close()

    session['default_supplier'] = current_supplier.get_name() + ' is set as default for ' + current_supplier.get_stock()

    return redirect(url_for('kin.stock'))

