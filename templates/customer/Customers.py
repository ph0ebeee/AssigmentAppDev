from users import Users 
import pyodbc

class Customers(Users.Users):
    #retrieve database for the count_id --USE WINDOWS--
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

    def __init__(self, first_name, last_name, email, password, gender, membership, orders, address, card_details):
        super().__init__(first_name, last_name, email, password, gender, membership, orders)
        self.__address = address
        self.__card_details = card_details

    def get_address(self):
        return self.__address

    def get_card_details(self):
        return self.__card_details

    def set_address(self, address):
        self.__address = address

    def set_card_details(self, card_details):
        self.__card_details = card_details
