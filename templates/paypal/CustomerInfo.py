# Payment by Wong Jun Yu Phoebe 210527H

from users import Users


class CustomerInfo(Users.Users):
    count_id = 0

    def __init__(self, name, email, address, card_no, expiry, expiry_month, cvv):
        super().__init__(None, name, email, None, None, address)
        CustomerInfo.count_id += 1
        self.__id = None
        self.__password = None
        self.__membership = None
        self.__gender = None
        self.__customerInfo_id = CustomerInfo.count_id
        self.__card_no = card_no
        self.__expiry = expiry
        self.__cvv = cvv
        self.__expiry_month = expiry_month

    def set_customer_id(self, customer_id):
        self.__customerInfo_id = customer_id

    def set_card_no(self, card_no):
        self.__card_no = card_no

    def set_expiry(self, expiry):
        self.__expiry = expiry

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_expiry_month(self, expiry_month):
        self.__expiry_month = expiry_month

    def get_expiry_month(self):
        return self.__expiry_month

    def get_card_no(self):
        return self.__card_no

    def get_expiry(self):
        return self.__expiry

    def get_cvv(self):
        return self.__cvv

    def get_customer_id(self):
        return self.__customerInfo_id
