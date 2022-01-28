#import database from sql server
import pyodbc
from forms.forms import signupForm
import bcrypt

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

#function to validate whether email input by user has recorded in the database
def validate_signUp_email(email):
    emailList = []
    form = signupForm(csrf_enabled=False)
    user_email = form.email
    cursor = conn.cursor()
    cursor.execute('SELECT EmailAddr from Staff')

    cursor_data = cursor.fetchall()

    cursor1 = conn.cursor()
    cursor1.execute('SELECT EmailAddr from Customer')

    cursor_data1 = cursor1.fetchall()

    for i in cursor_data:
        emailList.append(i)

    for i in cursor_data1:
        emailList.append(i)
    
    for i in emailList:
        if (email == i):
            return True
            break
        return False

def create_new_customer(name, email, passwd, contactnum, addr, postalCode):
    passwordList = []
    form = signupForm(csrf_enabled=False)
    password = form.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    salt = salt.decode('UTF-8')
    hashed = hashed.decode('UTF-8')
    print(hashed) #try
    # update the new information onto the SQL
    query = "INSERT INTO Customer (CustomerName, EmailAddr, Password, passwordSalt, ContactNum, ShippingAddr, PostalCode) OUTPUT INSERTED.CustomerID VALUES('{}','{}', '{}', '{}' , {}, '{}', {})".format(name, email, hashed, salt, contactnum, addr, postalCode)
    
