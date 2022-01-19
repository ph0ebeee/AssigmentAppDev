from users import Users
import pyodbc

class Staffs(Users.Users):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

    def __init__(self, id, name, email, remarks):
        super().__init__(id, name, email)
        self.__remarks = remarks

    #set
    def set_remarks(self,remarks):
        self.__remarks = remarks

    #get
    def get_remarks(self):
        return self.__remarks


