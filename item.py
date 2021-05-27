class Stock_item:
    count_id = 0
    quantity = 0

    def __init__(self, stock_name, price, origin, weight, dietary, ingre, description, amt_of_stock, category, brand,
                 unit, stock_unit):
        self.__amount = 0
        self.__id = Stock_item.count_id
        self.__stock_name = stock_name
        self.__price = price
        self.__origin = origin
        self.__weight = weight
        self.__dietary = dietary
        self.__ingredients = ingre
        self.__description = description
        self.__amt_of_stock = amt_of_stock
        self.__stock_left = amt_of_stock
        self.__category = category
        self.__total = 0
        self.__brand = brand
        self.__unit = unit
        self.__default_suppliers = ''
        self.__stock_unit = stock_unit
        self.__per_box = 0
        self.__per_box_working = 0

    def get_per_box(self):
        return self.__per_box

    def get_stock_unit(self):
        return self.__stock_unit

    def get_default_suppliers(self):
        return self.__default_suppliers

    def get_unit(self):
        return self.__unit

    def get_id(self):
        return int(self.__id)

    def get_stock_name(self):
        return self.__stock_name

    def get_total(self):
        self.__total = self.__amount * int(self.__price)
        return self.__total

    def get_origin(self):
        return self.__origin

    def get_dietary(self):
        return self.__dietary

    def get_weight(self):
        return self.__weight

    def get_ingredients(self):
        return self.__ingredients

    def get_description(self):
        return self.__description

    def get_amt_of_stock(self):
        return self.__amt_of_stock

    def get_stock_left(self):
        return int(self.__stock_left)

    def get_percentage(self):
        print(self.__stock_left, self.__amt_of_stock)
        percentage = (int(self.__stock_left) / int(self.__amt_of_stock)) * 100
        return int(round(percentage))

    def get_cat(self):
        return self.__category

    def get_base_price(self):
        return self.__price

    def get_category(self):
        return self.__category

    def get_brand(self):
        return self.__brand

    def set_brand(self, brand):
        self.__brand = brand

    def set_stock_name(self, stock_name):
        self.__stock_name = stock_name

    def set_base_price(self, price):
        self.__price = price

    def set_origin(self, origin):
        self.__origin = origin

    def set_dietary(self, dietary):
        self.__dietary = dietary

    def set_weight(self, weight):
        self.__weight = weight

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients

    def set_description(self, description):
        self.__description = description

    def set_amt_of_stock(self, amt_of_stock):
        self.__amt_of_stock = amt_of_stock

    def set_stock_left(self, stock_left):
        self.__stock_left = stock_left

    def set_id(self, id):
        self.__id = id

    def set_cat(self, cat):
        self.__category = cat

    def set_unit(self, unit):
        self.__unit = unit

    def set_amount_empty(self):
        self.__amount = 0

    def set_default_supplier(self, supplier):
        self.__default_suppliers = supplier

    def set_stock_unit(self, stock_unit):
        self.__stock_unit = stock_unit

    def set_per_box(self, per_box):
        self.__per_box = per_box

    def add_amount(self):
        self.__amount += 1

    def minus(self):
        self.__amount -= 1

    def get_amount(self):
        return self.__amount

    def decrease_stock(self):
        value = float(self.__stock_left)
        if self.__stock_unit == 'Kg' or self.__stock_unit == 'L':
            value -= self.__weight
            self.__stock_left = value
        elif self.__stock_unit == 'boxes':
            stock_in_box = self.__per_box_working
            stock_in_box += 1/int(self.__per_box)
            if stock_in_box >= 1:
                print('test')
                self.__stock_left -= 1
                stock_in_box -= 1
                self.__per_box_working = stock_in_box
            self.__per_box_working = stock_in_box

    def increase_stock(self, amt):
        self.__stock_left += int(amt)
        if self.__stock_left > self.__amt_of_stock:
            self.__amt_of_stock = self.__stock_left


class Restock:
    count_id = 0

    def __init__(self, email, order_number):
        Restock.count_id += 1
        self.__id = Restock.count_id
        self.__email = email
        self.__order_number = order_number

    def get_id(self):
        return self.__id

    def get_email(self):
        return self.__email

    def get_order(self):
        return self.__order_number

    def set_email(self, email):
        self.__email = email

    def set_order(self, order):
        self.__order_number = order

    def set_id(self, id):
        self.__id = id


class Order_delivery:
    count_id = 0

    def __init__(self, name, number, postal, address, level, door_no, card_no, exp_date, cvv, card_type, location,
                 remarks):
        Order_delivery.count_id += 1
        self.__id = Order_delivery.count_id
        self.__name = name
        self.__phone_no = number
        self.__postal = postal
        self.__address = address
        self.__level = level
        self.__door_no = door_no
        self.__card_no = card_no
        self.__exp_Date = exp_date
        self.__cvv = cvv
        self.__card = card_type
        self.__location = location
        self.__date = ""
        self.__remark = remarks
        self.__status = 'unassigned'
        self.__items = ""

    def get_name(self):
        return self.__name

    def get_remark(self):
        return self.__remark

    def get_location(self):
        return self.__location

    def get_phone(self):
        return self.__phone_no

    def get_postal(self):
        return self.__postal

    def get_address(self):
        return self.__address

    def get_level(self):
        return self.__level

    def get_door(self):
        return self.__door_no

    def get_card_no(self):
        return self.__card_no

    def get_exp_date(self):
        return self.__exp_Date

    def get_cvv(self):
        return self.__cvv

    def get_id(self):
        return self.__id

    def get_card(self):
        return self.__card

    def get_date(self):
        return self.__date

    def get_status(self):
        return self.__status

    def get_item(self):
        return self.__items

    def set_card(self, card):
        self.__card = card

    def set_id(self, id):
        self.__id = id

    def set_date(self, date):
        self.__date = date

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__phone_no = phone

    def set_postal(self, postal):
        self.__postal = postal

    def set_address(self, address):
        self.__address = address

    def set_level(self, level):
        self.__level = level

    def set_door_no(self, door):
        self.__door_no = door

    def set_exp(self, exp):
        self.__exp_Date = exp

    def set_ccv(self, cvv):
        self.__cvv = cvv

    def set_card_no(self, no):
        self.__card_no = no

    def set_location(self, location):
        self.__location = location

    def set_remark(self, remark):
        self.__remark = remark

    def set_status(self, status):
        self.__status = status

    def set_item(self, item):
        self.__items = item


class Order_self:
    count_id = 0

    def __init__(self, name, number, card_no, exp, cvv, card_type):
        Order_self.count_id += 1
        self.__id = Order_self.count_id
        self.__name = name
        self.__number = number
        self.__card_no = card_no
        self.__exp = exp
        self.__cvv = cvv
        self.__date = ""
        self.__location = ""
        self.__time = ""
        self.__card = card_type
        self.__status = 'not collected'
        self.__items = ""
        self.__general_location = ''

    def get_general_location(self):
        return self.__general_location

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def get_card_no(self):
        return self.__card_no

    def get_exp(self):
        return self.__exp

    def get_date(self):
        return self.__date

    def get_location(self):
        return self.__location

    def get_time(self):
        return self.__time

    def get_id(self):
        return self.__id

    def get_cvv(self):
        return self.__cvv

    def get_card(self):
        return self.__card

    def get_status(self):
        return self.__status

    def get_item(self):
        return self.__items

    def set_date(self, date):
        self.__date = date

    def set_location(self, location):
        self.__location = location

    def set_time(self, time):
        self.__time = time

    def set_card(self, card):
        self.__card = card

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__number = phone

    def set_ccv(self, cvv):
        self.__cvv = cvv

    def set_card_no(self, no):
        self.__card_no = no

    def set_status(self, status):
        self.__status = status

    def set_item(self, item):
        self.__items = item

    def set_general_location(self, location):
        self.__general_location = location


class Supplier:
    def __init__(self, name, email, phone, location):
        self.__id = 1
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__location = location
        self.__supplier_for_stock = ""

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_location(self):
        return self.__location

    def get_stock(self):
        return self.__supplier_for_stock

    def set_stock(self, stock):
        self.__supplier_for_stock = stock

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_number(self, number):
        self.__number = number

    def set_email(self, email):
        self.__email = email

    def set_location(self, location):
        self.__location = location
