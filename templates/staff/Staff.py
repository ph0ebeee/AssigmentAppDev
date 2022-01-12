from users import Users
import pyodbc

class Staff(Users.Users):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

    def __init__(self, first_name, last_name, email, password, phone_number):
        super().__init__(first_name, last_name, email, password)
        self.__phone_number = phone_number

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number


