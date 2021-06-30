import shelve

from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint

import Location
import User
from Forms import SignUp, Login, CreateLocation, UpdateProfile, UpdatePassword

elly = Flask(__name__)
elly.secret_key = 'any_random_string'
elly.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
elly.config["SESSION_PERMANENT"] = False
elly = Blueprint('elly', __name__, template_folder='templates', static_folder='static')

@elly.route('/loginActivity(cust)')
def loginActivity():
    return render_template('loginActivity(cust).html')


@elly.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUp(request.form)
    if request.method == 'POST' and signup_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            if key == signup_form.email.data:
                flash("Account already exist")
                return redirect(url_for('home'))

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User.User(signup_form.first_name.data, signup_form.last_name.data, signup_form.email.data,
                         signup_form.password.data)
        print("===user====", user)
        users_dict[user.get_email()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']

        user = users_dict[user.get_email()]
        print(user.get_first_name(), user.get_last_name(), "was stored in storage.db successfully with user_id ==",
              user.get_user_id())

        db.close()

        session['user_created'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('elly.login'))

    return render_template('signup(customer).html', form=signup_form)


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
            print(deliveryman_login)
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

    return render_template('login.html', form=login_form)


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
