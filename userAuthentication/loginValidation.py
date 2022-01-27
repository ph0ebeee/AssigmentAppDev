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
        #declaration of variables
        customerEmail_Password = {}

        #code to execute SQL code for Customer's email & password
        cursor = conn.cursor()
        cursor.execute('SELECT EmailAddr,Password,passwordSalt from Customer')

        #code to fetch result of the SQL code output for Customer's email
        cursor_data = cursor.fetchall()

        #change the Customer data format in dictionary form
        for i in cursor_data:
            customerEmail_Password.update( {i[0]:[i[1],i[2]]} )

        try:
            passwordEncode = password.encode("utf-8")
            passwordSalt = (customerEmail_Password[email][1]).encode("utf-8")
            hashedPw = bcrypt.hashpw(passwordEncode, passwordSalt)
            hashedPw = hashedPw.decode('UTF-8')
            #validation
            for i in customerEmail_Password:
                if (email == i) and (customerEmail_Password[i][0] == hashedPw):
                   return True
                   break
                return False
        except:
            return False

    def validated_Cust_Details(email, password):
        #declaration of variables
        customerDetails = []
        passwordEncode = password.encode("utf-8")
        hashedPw = bcrypt.hashpw(passwordEncode, bcrypt.gensalt())
        hashedPw = hashedPw.decode('UTF-8')
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


    def validate_staff_login(email, password):
        #declaration of variables
        staffEmail_Password = {}

        #code to execute SQL code for Staff email
        cursor = conn.cursor()
        cursor.execute('SELECT EmailAddr,Password, passwordSalt from Staff')

        cursor_data = cursor.fetchall()

        #change the Staff data format in dictionary form
        for i in cursor_data:
            staffEmail_Password.update( {i[0]:[i[1],i[2]]} )
        try:
            passwordEncode = password.encode("utf-8")
            passwordSalt = (staffEmail_Password[email][1]).encode("utf-8")
            hashedPw = bcrypt.hashpw(passwordEncode, passwordSalt)
            hashedPw = hashedPw.decode('UTF-8')
            #validation
            for i in staffEmail_Password:
                if (email == i) and (staffEmail_Password[i][0] == hashedPw):
                   return True
                   break
                return False
        except:
            return False

    def validated_Staff_Details(email, password):
        #declaration of variables
        staffDetails = []
        passwordEncode = password.encode("utf-8")
        hashedPw = bcrypt.hashpw(passwordEncode, bcrypt.gensalt())
        hashedPw = hashedPw.decode('UTF-8')
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
