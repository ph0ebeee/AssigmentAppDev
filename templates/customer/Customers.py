from users import Users 
import pyodbc

class Customers(Users.Users):
    #retrieve database for the count_id --USE WINDOWS--
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

    def __init__(self, id, name, email, password, membership, contactNum, address, postalcode):
        super().__init__(id, name, email, password, membership)
        self.__address = address
        self.__contactNum = contactNum
        self.__postalCode = postalcode

    def get_address(self):
        return self.__address

    #def get_card_details(self):
    #    return self.__card_details

    def get_contactNum(self):
        return self.__contactNum

    def set_address(self, address):
        self.__address = address

    #def set_card_details(self, card_details):
    #    self.__card_details = card_details

    def set_contactNum(self, contactNum):
        self.__contactNum = contactNum

    def get_postalCode(self):
        return self.__postalCode

    def get_postalCode(self):
        return self.__postalCode
