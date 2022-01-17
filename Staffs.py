from users import Users
import pyodbc

class Staffs(Users.Users):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

    def __init__(self, id, name, email, role, address, remarks):
        super().__init__(id, name, email)
        self.__address = address
        self.__role = role
        self.__remarks = remarks

    #set
    def set_address(self, address):
        self.__address = address

    def set_role(self,role):
        self.__role = role

    def set_remarks(self,remarks):
        self.__remarks = remarks

    #get
    def get_role(self):
        return self.__role

    def get_remarks(self):
        return self.__remarks

    def get_address(self):
        return self.__address



