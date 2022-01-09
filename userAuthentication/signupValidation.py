#import database from sql server
import pyodbc

from forms.forms import signupForm

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

#function to validate whether email input by user has recorded in the database
def validate_signUp_email():
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
        print(i)

    for i in emailList:
        if user_email == i:
            print("email is already registered ")
        else:
            print("no")
            break

validate_signUp_email()
#retrieve every single email in database and store it in a list
#use for loop to check if the email user entered for login matches the email addresses in the database
