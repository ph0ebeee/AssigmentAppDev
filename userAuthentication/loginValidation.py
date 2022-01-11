#Viona 211285T
#import database from sql server
import pyodbc
import customer.Customers
from flask import url_for
from werkzeug.utils import redirect

from forms.forms import loginForm

#connect SQL to python
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

#function to validate whether email and password input by user == input in the database
def validate_cust_login():
    #declaration of variables
    form = loginForm(csrf_enabled=False)
    user_email = form.email 
    user_password = form.password
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
        if user_email == i and user_password == customerEmail_Password[i]:
           return True
           break
        return False

def validated_Cust_Details():
    #declaration of variables
    form = loginForm(csrf_enabled=False)
    user_email = form.email 
    user_password = form.password
    customerDetails = []

    #code to execute SQL code for Customer's email    
    cursor = conn.cursor()
    query = 'SELECT * from Customer WHERE EmailAddr="{}" AND Password="{}"'.format(user_email,user_password)
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        customerDetails.append(i)    

    return customerDetails


def validate_staff_login():
    #declaration of variables
    form = loginForm(csrf_enabled=False)
    user_email = form.email 
    user_password = form.password
    staffEmail_Password = {}

    #code to execute SQL code for Staff email
    cursor = conn.cursor()
    cursor.execute('SELECT EmailAddr,Password from Staff')


    #change the Staff data format in dictionary form
    for i in cursor_data:
        staffEmail_Password.update( {i[0]:i[1]} )
    
    #validation
    for i in staffEmail_Password:
        if user_email == i and user_password == staffEmail_Password[i]:
            return True
            break
        return False

def validated_Staff_Details():
    #declaration of variables
    form = loginForm(csrf_enabled=False)
    user_email = form.email 
    user_password = form.password
    staffDetails = []

    #code to execute SQL code for Customer's email    
    cursor = conn.cursor()
    query = "SELECT * from Staff WHERE EmailAddr='{}' AND Password='{}'".format(user_email,user_password)
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
