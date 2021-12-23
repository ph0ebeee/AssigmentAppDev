class Users:
    def __init__(self, first_name, last_name, email, password, username, gender, membership, orders):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password
        self.username = username
        self.__gender = gender
        self.__membership = membership
        self.__orders = orders

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_username(self):
        return self.username

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_orders(self):
        return self.__orders

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_username(self, username):
        self.username = username

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_orders(self, orders):
        self.__orders = orders
