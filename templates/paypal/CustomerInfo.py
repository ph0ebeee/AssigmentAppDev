from users import Users

class CustomerInfo(Users.Users):
    def __init__(self,id,name,address,card_no,expiry,cvc):
        super().__init__(id,name,address,)
        self.__card_no = card_no
        self.__expiry = expiry
        self.__cvc = cvc

    def set_card_no(self,card_no):
        self.__card_no = card_no

    def set_expiry(self,expiry):
        self.__expiry = expiry

    def set_cvc(self,cvc):
        self.__cvc = cvc

    def get_card_no(self):
        return self.__card_no

    def get_expiry(self):
        return self.__expiry

    def get_cvc(self):
        return self.__cvc

