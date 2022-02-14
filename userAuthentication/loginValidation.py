#Viona 211285T
#import database from sql server
import pyodbc
import bcrypt
#import customer.Customers
from flask import url_for
from werkzeug.utils import redirect
from forms.forms import loginForm
#connect SQL to python

try:
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')
    #function to validate whether email and password input by user == input in the database
    def validate_cust_login(email, password):
        #code to execute SQL code for Staff email
        cursor = conn.cursor()
        query = "SELECT PasswordSalt, Password from Customer WHERE EmailAddr = '{}'".format(email)
        cursor.execute(query)

        cursor_data = cursor.fetchall()
        saltList = []
        #change the Staff data format in dictionary form
        for i in cursor_data:
            saltList.append(i)
        if len(saltList) != 0:
            for i in saltList:
                passwordEncode = password.encode("utf-8")
                passwordSalt = (i[0]).encode("utf-8")
                hashedPw = bcrypt.hashpw(passwordEncode, passwordSalt)
                hashedPw = hashedPw.decode('UTF-8')
                if hashedPw == i[1]:
                    return True
                else:
                    return False
        else:
            return False

    def validated_Cust_Details(email):
        #declaration of variables
        customerDetails = []
        #code to execute SQL code for Customer's email    
        cursor = conn.cursor()
        query = "SELECT * from Customer WHERE EmailAddr='{}'".format(email)
        cursor.execute(query) #error pyodbc.ProgrammingError: ('42000', "[42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]Incorrect syntax near '$2'. (102) (SQLExecDirectW)"

        #code to fetch result of the SQL code output for Customer's email
        cursor_data = cursor.fetchall()

        #change the Customer data format in dictionary form
        for i in cursor_data:
            customerDetails.append(i)    

        return customerDetails

    def validated_Cust_Details_id(id):
        #declaration of variables
        customerDetails = []
        #code to execute SQL code for Customer's email    
        cursor = conn.cursor()
        query = "SELECT * from Customer WHERE CustomerID='{}'".format(id)
        cursor.execute(query) #error pyodbc.ProgrammingError: ('42000', "[42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]Incorrect syntax near '$2'. (102) (SQLExecDirectW)"

        #code to fetch result of the SQL code output for Customer's email
        cursor_data = cursor.fetchall()

        #change the Customer data format in dictionary form
        for i in cursor_data:
            customerDetails.append(i)    

        return customerDetails

    def validate_staff_login(email, password):
        #code to execute SQL code for Staff email
        cursor = conn.cursor()
        query = "SELECT PasswordSalt, Password from Staff WHERE EmailAddr = '{}'".format(email)
        cursor.execute(query)

        cursor_data = cursor.fetchall()
        saltList = []
        #change the Staff data format in dictionary form
        for i in cursor_data:
            saltList.append(i)
        if len(saltList) != 0:
            for i in saltList:
                passwordEncode = password.encode("utf-8")
                passwordSalt = (i[0]).encode("utf-8")
                hashedPw = bcrypt.hashpw(passwordEncode, passwordSalt)
                hashedPw = hashedPw.decode('UTF-8')
                if hashedPw == i[1]:
                    return True
                else:
                    return False
        else:
            return False

    def validated_Staff_Details(email):
        #declaration of variables
        staffDetails = []
        #code to execute SQL code for Customer's email    
        cursor = conn.cursor()
        query = "SELECT * from Staff WHERE EmailAddr='{}'".format(email)
        cursor.execute(query)
  
        #code to fetch result of the SQL code output for Customer's email
        cursor_data = cursor.fetchall()

        #change the Customer data format in dictionary form
        for i in cursor_data:
            staffDetails.append(i)    
            return staffDetails
except:
    print('Error retrieving database')
