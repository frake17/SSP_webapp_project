import shelve

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint

import User
from Forms import CreateDeliverymen, \
    self_collection_update, deliverymen_status_update, deliverymen_profile_update

qing = Flask(__name__)
qing.secret_key = 'any_random_string'
qing.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
qing.config["SESSION_PERMANENT"] = False
qing = Blueprint('qing', __name__, template_folder='templates', static_folder='static')


@qing.route('/orders', methods=['GET', 'POST'])
def orders():
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
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'W':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'West':
            order_list.append(order_deliver)

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
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'N':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'North':
            order_list.append(order_deliver)
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
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'S':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'South':
            order_list.append(order_deliver)
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
    for key in deliverymen_dict:
        deliverymen = deliverymen_dict.get(key)
        if deliverymen.get_regions() == 'E':
            deliverymen_list.append(deliverymen)

    for key in order_dict:
        order_deliver = order_dict.get(key)
        if order_deliver.get_location() == 'East':
            order_list.append(order_deliver)

    return render_template('Dest_East.html', deliveryman_list=deliverymen_list, order_list=order_list)


@qing.route('/All_Deliveries')
def All_Deliveries():
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
    count = 1
    create_Deliverymen_form = CreateDeliverymen(request.form)
    if request.method == 'POST' and create_Deliverymen_form.validate():
        deliverymen_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            deliverymen_dict = db["Deliverymen"]
            while count in deliverymen_dict:
                count += 1
        except:
            print("Error in retrieving Users from storage.db.")

        deliverymen = User.Deliverymen(create_Deliverymen_form.first_name.data, create_Deliverymen_form.last_name.data,
                                       create_Deliverymen_form.email.data, create_Deliverymen_form.gender.data,
                                       create_Deliverymen_form.contact_no.data, create_Deliverymen_form.regions.data,
                                       create_Deliverymen_form.remarks.data)

        deliverymen_dict[deliverymen.get_Deliverymen_id()] = deliverymen
        db['Deliverymen'] = deliverymen_dict
        deliverymen_login = {}
        try:
            deliverymen_login = db["Deliverymen_login"]
        except:
            print("Error in retrieving Deliverymen from storage.db")

        deliverymen_login[create_Deliverymen_form.email.data] = deliverymen.get_Deliverymen_id()
        db["Deliverymen_login"] = deliverymen_login
        db.close()

        session['Deliverymen_created'] = deliverymen.get_first_name() + ' ' + deliverymen.get_last_name()
        return redirect(url_for('qing.Display_Deliverymen'))

    return render_template('Create_Deliverymen.html', form=create_Deliverymen_form)


@qing.route('/Display_Deliverymen', defaults={'id': None})
@qing.route('/Display_Deliverymen/<int:id>')
def Display_Deliverymen(id):
    users_dict = {}
    order_list = {}
    db = shelve.open('storage.db', 'r')
    try:
        users_dict = db['Deliverymen']
        assign_dict = db['assignDeliverymen']
        if id is not None:
            order_list = assign_dict.get(id)

    except:
        print("Error in displaying Users from storage.db.")
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('Display_Deliverymen.html', count=len(users_list), users_list=users_list,
                           order_list=order_list)


@qing.route('/updateDeliverymen/<int:id>/', methods=['GET', 'POST'])
def update_Deliverymen(id):
    update_Deliverymen_form = CreateDeliverymen(request.form)
    if request.method == 'POST' and update_Deliverymen_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Deliverymen']

        user = users_dict.get(id)
        user.set_first_name(update_Deliverymen_form.first_name.data)
        user.set_last_name(update_Deliverymen_form.last_name.data)
        user.set_gender(update_Deliverymen_form.gender.data)
        user.set_email(update_Deliverymen_form.email.data)
        user.set_contact_no(update_Deliverymen_form.contact_no.data)
        user.set_regions(update_Deliverymen_form.regions.data)
        user.set_remarks(update_Deliverymen_form.remarks.data)

        db['Deliverymen'] = users_dict
        db.close()

        session['Deliverymen_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('qing.Display_Deliverymen'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Deliverymen']
        db.close()

        user = users_dict.get(id)
        update_Deliverymen_form.first_name.data = user.get_first_name()
        update_Deliverymen_form.last_name.data = user.get_last_name()
        update_Deliverymen_form.gender.data = user.get_gender()
        update_Deliverymen_form.email.data = user.get_email()
        update_Deliverymen_form.contact_no.data = user.get_contact_no()
        update_Deliverymen_form.regions.data = user.get_regions()
        update_Deliverymen_form.remarks.data = user.get_remarks()

        return render_template('updateDeliverymen.html', form=update_Deliverymen_form)


@qing.route('/deleteDeliverymen/<int:id>', methods=['POST'])
def delete_Deliverymen(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Deliverymen']
    deliveryman_login = db['Deliverymen_login']

    user = users_dict.pop(id)
    deliveryman_login.pop(user.get_email())

    db['Deliverymen'] = users_dict
    db.close()

    session['Deliverymen_deleted'] = user.get_first_name() + ' ' + user.get_last_name()

    return redirect(url_for('qing.Display_Deliverymen'))


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
    users_dict = db['Deliverymen']
    order_dict = db['confirmed_delivery']

    print(order_dict)
    assign_dict = {}
    try:
        assign_dict = db['assignDeliverymen']

        if id in assign_dict:
            order_list = assign_dict.get(id)
            print(order_list)

    except:
        print('No database')
    deliverymen = users_dict.get(id)
    current_order = order_dict.get(orderid)
    print('**', current_order)
    current_order.set_status('assign')
    order_list.append(current_order)
    print('***', order_list)
    assign_dict[deliverymen.get_Deliverymen_id()] = order_list
    db['assignDeliverymen'] = assign_dict
    db['confirmed_delivery'] = order_dict
    db.close()
    session['OrdersID_assigned'] = deliverymen.get_Deliverymen_id()
    session['Orders_assigned'] = deliverymen.get_first_name() + deliverymen.get_last_name()
    if NSEW == 'North':
        return redirect(url_for('qing.Dest_North'))
    elif NSEW == 'South':
        return redirect(url_for('qing.Dest_South'))
    elif NSEW == 'East':
        return redirect(url_for('qing.Dest_East'))
    elif NSEW == 'West':
        return redirect(url_for('qing.Dest_West'))


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
        print(users_dict)
        print(user.get_name(), user.get_number())
        updateSelfCollection_form.name.data = user.get_name()
        updateSelfCollection_form.number.data = user.get_number()
        print(updateSelfCollection_form.name.data)
        print(updateSelfCollection_form.number.data)

        return render_template('updateSelfCollection.html', form=updateSelfCollection_form)


@qing.route('/ordersAssigned/<int:id>/', methods=['GET', 'POST'])
def ordersAssigned(id):
    index = 0
    db = shelve.open('storage.db', 'r')
    assign_deliverymen = {}
    ordersAssigned_list = []
    try:
        assign_deliverymen = db['assignDeliverymen']
        if id in assign_deliverymen:
            ordersAssigned_list = assign_deliverymen.get(id)
        else:
            ordersAssigned_list = []
    except:
        print('anything')
        return render_template(url_for('qing.Display_Deliverymen'))
    deliverymen_id = id
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


@qing.route('/deliverymen_update_status/<int:id>/', methods=['GET', 'POST'])
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


@qing.route('/deliverymen_update_profile/<int:id>/', methods=['GET', 'POST'])
def deliverymen_update_profile(id):
    deliverymen_update_profile_form = deliverymen_profile_update(request.form)
    if request.method == 'POST' and deliverymen_update_profile_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Deliverymen']

        user = users_dict.get(id)
        user.set_first_name(deliverymen_update_profile_form.first_name.data)
        user.set_last_name(deliverymen_update_profile_form.last_name.data)
        user.set_gender(deliverymen_update_profile_form.gender.data)
        user.set_email(deliverymen_update_profile_form.email.data)
        user.set_contact_no(deliverymen_update_profile_form.contact_no.data)
        user.set_regions(deliverymen_update_profile_form.regions.data)
        user.set_remarks(deliverymen_update_profile_form.remarks.data)

        db['Deliverymen'] = users_dict
        db.close()

        session['Deliverymen_Profile_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('qing.DeliverymenProfile'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Deliverymen']
        db.close()

        user = users_dict.get(id)
        deliverymen_update_profile_form.first_name.data = user.get_first_name()
        deliverymen_update_profile_form.last_name.data = user.get_last_name()
        deliverymen_update_profile_form.gender.data = user.get_gender()
        deliverymen_update_profile_form.email.data = user.get_email()
        deliverymen_update_profile_form.contact_no.data = user.get_contact_no()
        deliverymen_update_profile_form.regions.data = user.get_regions()
        deliverymen_update_profile_form.remarks.data = user.get_remarks()

        return render_template('deliverymen_update_profile.html', form=deliverymen_update_profile_form)


@qing.route('/deliverymen_orders')
def deliverymen_orders():
    email = session.get('current')
    db = shelve.open('storage.db', 'r')
    deliverymen_login = db["Deliverymen_login"]
    assign_orders = db['assignDeliverymen']
    current_id = deliverymen_login.get(email)
    print(current_id)
    orders_list = assign_orders.get(current_id)
    print(orders_list)
    return render_template('ordersAssigned(deliveryman).html', orders_list=orders_list)


@qing.route('/DeliverymenProfile', methods=['GET', 'POST'])
def DeliverymenProfile():
    email = session.get('current')
    db = shelve.open('storage.db', 'r')
    deliverymen_login = db["Deliverymen_login"]
    Deliverymen_dict = db['Deliverymen']
    current_id = deliverymen_login.get(email)
    Deliverymen_list = []
    Deliverymen = Deliverymen_dict.get(current_id)
    Deliverymen_list.append(Deliverymen)
    return render_template('DeliverymenProfile.html', users_list=Deliverymen_list)
