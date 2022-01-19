class Users:
    count_id = 0

    def __init__(self, id, name, email, password, membership, gender, address):
        Users.count_id += 1
        self.__id = id
        self.__name = name
        self.__gender = gender
        self.__email = email
        self.__password = password
        self.__membership = membership
        self.__address = address
        #self.__orders = orders

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_membership(self):
        return self.__membership

    def set_address(self,address):
        self.__address = address

    def get_address(self):
        return self.__address

    #def get_orders(self):
    #    return self.__orders
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_gender(self,gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_membership(self, membership):
        self.__membership = membership

    #def set_orders(self, orders):
    #    self.__orders = orders


def query():
    pass
    #idk


def query():
    pass
    #idk


def query():
    pass
    #idk
