class User:
    count_id = 0

    def __init__(self, first_name, last_name, email, password):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password


class Login:
    def __init__(self, email, password):
        self.__email = email
        self.__password = password

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password


class Deliverymen:
    count_id = 0

    def __init__(self, first_name, last_name, email, gender, contact_no, regions, remarks):
        Deliverymen.count_id += 1
        self.__Deliverymen_id = Deliverymen.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__contact_no = contact_no
        self.__regions = regions
        self.__remarks = remarks

    def get_Deliverymen_id(self):
        return self.__Deliverymen_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_contact_no(self):
        return self.__contact_no

    def get_regions(self):
        return self.__regions

    def get_remarks(self):
        return self.__remarks

    def set_Deliverymen_id(self, Deliverymen_id):
        self.__Deliverymen_id = Deliverymen_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_contact_no(self, contact_no):
        self.__contact_no = contact_no

    def set_regions(self, regions):
        self.__regions = regions

    def set_remarks(self, remarks):
        self.__remarks = remarks


class Temp:
    count_id = 0

    def __init__(self, outlet, date, cust_ic, cust_no, temp, time_enter, time_leave, status):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__outlet = outlet
        self.__date = date
        self.__cust_ic = cust_ic
        self.__cust_no = cust_no
        self.__temp = temp
        self.__time_enter = time_enter
        self.__time_leave = time_leave
        self.__status = status

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_outlet(self, outlet):
        self.__outlet = outlet

    def set_date(self, date):
        self.__date = date

    def set_cust_ic(self, cust_ic):
        self.__cust_ic = cust_ic

    def set_cust_no(self, cust_no):
        self.__cust_no = cust_no

    def set_temp(self, temp):
        self.__temp = temp

    def set_time_enter(self, time_enter):
        self.__time_enter = time_enter

    def set_time_leave(self, time_leave):
        self.__time_leave = time_leave

    def set_status(self, status):
        self.__status = status

    def get_user_id(self):
        return self.__user_id

    def get_outlet(self):
        return self.__outlet

    def get_date(self):
        return self.__date

    def get_cust_ic(self):
        return self.__cust_ic

    def get_cust_no(self):
        return self.__cust_no

    def get_temp(self):
        return self.__temp

    def get_time_enter(self):
        return self.__time_enter

    def get_time_leave(self):
        return self.__time_leave

    def get_status(self):
        return self.__status
