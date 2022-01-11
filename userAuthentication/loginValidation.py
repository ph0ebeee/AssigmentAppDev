#Viona 211285T
#import database from sql server
import pyodbc
<<<<<<< HEAD
=======
#import customer.Customers
from flask import url_for
from werkzeug.utils import redirect
>>>>>>> 5931283829a2b5414df722c4f0221a494c4fa99e

from forms.forms import loginForm

#connect SQL to python
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
    cursor.execute('SELECT EmailAddr,Password from Customer')

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        customerEmail_Password.update( {i[0]:i[1]} )
    
    #validation
    for i in customerEmail_Password:
        if email == i and password == customerEmail_Password[i]:
           return True
           break
        return False

def validated_Cust_Details(email, password):
    #declaration of variables
    customerDetails = []

    #code to execute SQL code for Customer's email    
    cursor = conn.cursor()
    query = "SELECT * from Customer WHERE EmailAddr='{}' AND Password='{}'".format(email,password)
    cursor.execute(query)

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
    cursor.execute('SELECT EmailAddr,Password from Staff')

    cursor_data = cursor.fetchall()

    #change the Staff data format in dictionary form
    for i in cursor_data:
        staffEmail_Password.update( {i[0]:i[1]} )
    
    #validation
    for i in staffEmail_Password:
        if email == i and password == staffEmail_Password[i]:
            return True
            break
        return False

def validated_Staff_Details(email, password):
    #declaration of variables
    staffDetails = []

    #code to execute SQL code for Customer's email    
    cursor = conn.cursor()
    query = "SELECT * from Staff WHERE EmailAddr='{}' AND Password='{}'".format(email,password)
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        staffDetails.append(i)    

    return staffDetails


#what i need to do {done}
#1. create a loop that checks users email and password input thru the staff and cust dictionary in 2 seperate loops
#2. if its correct staff will go staff customer go customer
