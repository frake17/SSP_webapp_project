from datetime import datetime, date

from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, DateField, \
    FloatField, TimeField, ValidationError, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf import Form, RecaptchaField


class Item(Form):
    stock_name = StringField('Stock Name', [validators.DataRequired()])
    brand = StringField('Brand Name', [validators.DataRequired()])
    amt_of_stock = IntegerField('Current stock', [validators.DataRequired()])
    stock_unit = SelectField('Unit for stocks', [validators.DataRequired()],
                             choices=[('Kg', 'Kg'), ('L', 'L'), ('boxes', 'boxes')], render_kw={'onchange': "myFunction()"})
    subcategory_boxes = IntegerField('Per box', [validators.Optional()])
    price = FloatField('Price', [validators.DataRequired()])
    origin = StringField('Origin', [validators.DataRequired()])
    weight = FloatField('Weight', [validators.DataRequired()])
    unit = SelectField('Unit', [validators.DataRequired()],
                       choices=[('Kg', 'Kg'), ('L', 'L')])
    Dietary = SelectField('Dietary', [validators.Optional()], choices=[
        ('', 'Select'), ('Halal', 'Halal'), ('Healthier choice', 'Healthier choice'), ('Organic', 'Organic'),
        ('Vegetarian', 'Vegetarian'),
        ('Gluten-Free', 'Gluten-Free'), ('Trans-Fat-Free', 'Trans-Fat-Free'), ('Hypoallergenic', 'Hypoallergenic'),
        ('Lactose-Free', 'Lactose-Free')
    ], default='')
    category = SelectField('Category', [validators.required()],
                           choices=[('Fruit and vegetables', 'Fruit and vegetables'), ('Frozen', 'Frozen'),
                                    ('Dairy', 'Dairy'), ('Meat and seafood', 'Meat and seafood'), ('Drinks', 'Drinks'),
                                    ('Packaged food and snacks', 'Packaged food and snacks')])
    ingredients = TextAreaField('Ingredients', [validators.Optional()])
    description = TextAreaField('Description', [validators.Optional()])

    def validate_amt_of_stock(form, amt_of_stock):
        if not str(amt_of_stock.data).isdigit():
            raise ValidationError('Only digits allowed')

    def validate_price(form, price):
        if type(price.data) != float:
            raise ValidationError('Only digits allowed')

    def validate_weight(form, weight):
        print(type(weight.data))
        if type(weight.data) != float:
            raise ValidationError('Only digits allowed')


class Order(Form):
    name = StringField('name', [validators.DataRequired()])
    number = IntegerField('Phone_number',
                          [validators.DataRequired()])
    postal = IntegerField('Postal_code', [validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    general_location = SelectField('General location', [validators.data_required()],
                                   choices=[('North', 'North'), ('South', 'South'),
                                            ('East', 'East'), ('West', 'West')])
    level = IntegerField('Level', [validators.number_range(min=1, max=50), validators.DataRequired()])
    door_number = StringField('Door_number', [validators.DataRequired()])
    card_number = IntegerField('Card_number', [
                                               validators.DataRequired()])
    exp_date = DateField('Exp_date(mm/yyyy)', [validators.DataRequired()], format='%m/%Y')
    cvv = IntegerField('Card_cvv', [validators.number_range(min=000, max=999), validators.DataRequired()])
    card_type = SelectField('Card_type', choices=[('CC', 'Credit Card'), ('DC', 'Debit Card')])
    remarks = TextAreaField('Remarks')

    def validate_number(form, number):
        length = str(number.data)
        if len(length) > 8 or len(length) < 8:
            raise ValidationError('Phone number should be 8 numbers')
        if not length.isdigit():
            raise ValidationError('Only digits are allowed')

    def validate_postal(form, postal):
        if not str(postal.data).isdigit():
            raise ValidationError('Only digits are allowed')
        if len(str(postal.data)) < 6 or len(str(postal.data)) > 6:
            raise ValidationError('Postal code is only 6 digits long')

    def validate_level(form, level):
        if not str(level.data).isdigit():
            raise ValidationError('Only digit allowed')

    def validate_card_number(form, card_number):
        if len(str(card_number.data)) > 19 or len(str(card_number.data)) < 16:
            raise ValidationError('Card numbers should be between 16 and 19')

    def validate_cvv(form, cvv):
        if len(str(cvv.data)) != 3:
            raise ValidationError('cvv should be 3 digits long')

    def validate_exp_date(self, exp_date):
        date_now = datetime.now()
        date = date_now.strftime('%Y-%m-%d')
        exp = exp_date.data.strftime('%Y-%m-%d')
        if exp < date:
            raise ValidationError('Expiry date is invalid')


class self_collect(Form):
    name = StringField('name', [validators.DataRequired()])
    card_number = IntegerField('Card number', [
                                               validators.DataRequired()])
    exp_date = DateField('Expiry date(mm/yyyy)', [validators.DataRequired()], format='%m/%Y')
    cvv = IntegerField('Card cvv', [validators.DataRequired()])
    card_type = SelectField('Card type', choices=[('CC', 'Credit Card'), ('DC', 'Debit Card')])
    number = IntegerField('Phone number',
                          [validators.DataRequired()])

    def validate_card_number(form, card_number):
        if len(str(card_number.data)) > 19 or len(str(card_number.data)) < 16:
            raise ValidationError('Card numbers should be between 16 and 19')

    def validate_cvv(form, cvv):
        if len(str(cvv.data)) != 3:
            raise ValidationError('cvv should be 3 digits long')

    def validate_number(form, number):
        length = str(number.data)
        if len(length) > 8 or len(length) < 8:
            raise ValidationError('Phone number should be 8 numbers')
        if not length.isdigit():
            raise ValidationError('Only digits are allowed')

    def validate_exp_date(self, exp_date):
        date_now = datetime.now()
        date = date_now.strftime('%Y-%m-%d')
        exp = exp_date.data.strftime('%Y-%m-%d')
        if exp < date:
            raise ValidationError('Expiry date is invalid')


class self_collection_update(Form):
    name = StringField('name', [validators.data_required()])
    number = IntegerField('Phone_number',
                          [validators.number_range(min=00000000, max=99999999,
                                                   message='Contact number should be 8 digits'),
                           validators.data_required()])
    status = SelectField('Status',
                         choices=[('collected', 'collected'), ('Not collected', 'Not collected'), ('reschedule', 'reschedule')])

    def validate_number(form, number):
        length = str(number.data)
        if len(length) > 8 or len(length) < 8:
            raise ValidationError('Phone number should be 8 numbers')
        if not length.isdigit():
            raise ValidationError('Only digits are allowed')


class Supplier(Form):
    name = StringField('name', [validators.DataRequired()])
    number = IntegerField('Phone_number',
                          [validators.DataRequired()])
    email = EmailField('email', [validators.DataRequired()])
    location = StringField('Location', [validators.DataRequired()])

    def validate_number(form, number):
        length = str(number.data)
        if len(length) > 8 or len(length) < 8:
            raise ValidationError('Phone number should be 8 numbers')
        if not length.isdigit():
            raise ValidationError('Only digits are allowed')


class recaptcha_form(Form):
    recaptcha = RecaptchaField()


class SignUp(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password')])
    security_question = SelectField('Security question', [validators.DataRequired()], choices = [('1', 'option 1'), ('2', 'option 2'), ('3', 'option 3')]
                                                                    )
    security_answer = StringField('Security answers', [validators.DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_password(form, password):
        password_value = password.data
        special_characters = False
        upper_case = False
        lower_case = False
        numeric_number = False
        if len((str(password_value ))) < 8:
            raise ValidationError('Password should be at least 8 letters/digits long')
        for i in str(password_value ):
            if i.isupper():
                upper_case = True
            if i.islower():
                lower_case = True
            if i.isdigit():
                numeric_number = True
            if not i.isalnum():
                special_characters = True
        if not upper_case:
            raise ValidationError('Password must contain at least 1 upper case letter')
        if not lower_case:
            raise ValidationError('Password must contain at least 1 lower case letter')
        if not numeric_number:
            raise ValidationError('Password must contain at least 1 digit')
        if not special_characters:
            raise ValidationError('Password must contain at least 1 special character')


class optional_signup(Form):
    Phone_number = IntegerField('Phone number', validators=(validators.Optional(),))
    card_number = IntegerField('Card number', validators=(validators.Optional(),))
    exp_date = DateField('Expiry date(mm/yyyy)',format='%m/%Y',validators=(validators.Optional(),))
    CVV = IntegerField('CVV', validators=(validators.Optional(),))


class Login(Form):
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Log In')


class UpdateProfile(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Email()])


class UpdatePassword(Form):
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')


class CreateLocation(Form):
    neighbourhood = StringField('Neighbourhood', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    area = RadioField('Area', choices=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
                      default='North')
    availability = RadioField('Availability', choices=[('Full', 'Full'), ('Available', 'Available')], default='Full')


class CreateDeliverymen(Form):
    first_name = StringField('First Name :', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name :', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender :', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField('Email :', [validators.Length(min=1, max=150), validators.DataRequired()])
    contact_no = IntegerField('Contact number :', [validators.DataRequired()])
    regions = RadioField('Regions in charge :', choices=[('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West')],
                         default='F')
    remarks = TextAreaField('Remarks :', [validators.Optional()])

    def validate_contact_no(form, contact_no):
        length = str(contact_no.data)
        if len(length) > 8 or len(length) < 8:
            raise ValidationError('Phone number should be 8 numbers')
        if not length.isdigit():
            raise ValidationError('Only digits are allowed')


class deliverymen_profile_update(Form):
    first_name = StringField('First Name :', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name :', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender :', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField('Email :', [validators.Length(min=1, max=150), validators.DataRequired()])
    contact_no = IntegerField('Contact number :', [validators.DataRequired()])
    regions = RadioField('Regions in charge :', choices=[('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West')],
                         default='F')
    remarks = TextAreaField('Remarks :', [validators.Optional()])

    def validate_contact_no(form, contact_no):
        length = str(contact_no.data)
        if len(length) > 8 or len(length) < 8:
            raise ValidationError('Phone number should be 8 numbers')
        if not length.isdigit():
            raise ValidationError('Only digits are allowed')


class deliverymen_status_update(Form):
    name = StringField('name', [validators.data_required()])
    number = IntegerField('Phone_number',[validators.data_required()])
    level = IntegerField('Level', [validators.number_range(min=1, max=50), validators.DataRequired()])
    door_number = IntegerField('Door_number', [validators.DataRequired()])
    postal = IntegerField('Postal_code', [validators.number_range(min=1, max=999999), validators.DataRequired()])

    def validate_number(form, number):
        length = str(number.data)
        if len(length) > 8 or len(length) < 8:
            raise ValidationError('Phone number should be 8 numbers')
        if not length.isdigit():
            raise ValidationError('Only digits are allowed')

    def validate_postal(form, postal):
        if not str(postal.data).isdigit():
            raise ValidationError('Only digits are allowed')
        if len(str(postal.data)) < 6 or len(str(postal.data)) > 6:
            raise ValidationError('Postal code is only 6 digits long')


class CreateUserForm(Form):
    date = DateField("Date (YYYY-MM-DD)", format='%Y-%m-%d', default=datetime.now())
    cust_ic = StringField("Customer IC", [validators.DataRequired()])
    cust_no = StringField("Customer Number", [validators.DataRequired()])
    temp = FloatField("Temperature (°C)", [
        validators.NumberRange(max=37.5, message="Temperature is above 37.5°C, customer not allowed to enter"),
        validators.DataRequired()])
    time_enter = TimeField("Time - Enter (HH:MM)", format='%H:%M', default=datetime.now())
    time_leave = TimeField("Time - Leave (HH:MM)", format='%H:%M', default=datetime.strptime("23:59", "%H:%M"))

    def validate_cust_ic(form, cust_ic):
        if not cust_ic.data.startswith(("S", "T")):
            raise ValidationError("IC must start with S or T")
        if not cust_ic.data[1:7].isdigit():
            raise ValidationError("IC must be in digits excluding first and last letters")
        if not cust_ic.data[-1].isalpha():
            raise ValidationError("IC must end with an alphabet")
        if len(cust_ic.data) != 9:
            raise ValidationError("Length of IC must be 9 characters")

    def validate_cust_no(form, cust_no):
        if not cust_no.data.isdigit():
            raise ValidationError("Customer's number must be all digits")
        if len(cust_no.data) != 8:
            raise ValidationError("Customer's number must only have 8 digits")


class SearchUserForm(Form):
    search_date = DateField("Date (YYYY-MM-DD)", format='%Y-%m-%d', default=datetime.now())
    search_cust = StringField("Customer IC")

    def validate_search_cust(form, search_cust):
        if not search_cust.data.startswith(("S", "T")):
            raise ValidationError("IC must start with S or T")
        if not search_cust.data[1:7].isdigit():
            raise ValidationError("IC must be in digits excluding first and last letters")
        if not search_cust.data[-1].isalpha():
            raise ValidationError("IC must end with an alphabet")
        if len(search_cust.data) != 9:
            raise ValidationError("Length of IC must be 9 characters")
