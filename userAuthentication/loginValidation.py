#import database from sql server
import pyodbc
from forms.py import loginForm

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

#function to validate whether email input by user has recorded in the database
def validate_login_email():
    emailList = []
    form = loginForm(csrf_enabled=False)
    user_email = form.email
    cursor = conn.cursor()
    cursor.execute('SELECT EmailAddr from Staff and Customer')

    cursor_data = cursor.fetchall()

    for i in cursor_data:
        emailList.append(i)

    for i in emailList:
        print(i)

    for i in emailList:
        if user_email == i:
            validate_login_password()   
        else:
            print('cannot')
            break

def validate_login_password():
    passwordList = []
    form = loginForm(csrf_enabled=False)
    user_password = form.password
    cursor1 = conn.cursor()
    cursor1.execute('SELECT Password from Staff and Customer')

    cursor_data1 = cursor1.fetchall()

    for i in cursor_data:
        passwordList.append(i)

    for i in emailList:
        print(i)

    for i in passwordList:
        if user_password == i:
            print('yes')   
        else:
            print('no')
            break

validate_login_email()
validate_login_password()