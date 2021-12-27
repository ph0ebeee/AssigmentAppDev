from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators
from wtforms.fields import EmailField, DateField
import pyodbc

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

## ONLY FOR SIGN UP, SEPARATE SIGN UP AND LOGIN VALIDATION


#class loginForm(Form):
#    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
#    password = PasswordField('Password', [validators.length(max=100), validators.DataRequired()])

class signupForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(max=100), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])

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
            print("yes")
        else:
            print("no")
            break

validate_signUp_email()
#retrieve every single email in database and store it in a list
#use for loop to check if the email user entered for login matches the email addresses in the database