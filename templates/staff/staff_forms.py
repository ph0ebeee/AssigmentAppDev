
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
#from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#from users import Users
from userAuthentication import signupValidation
import pyodbc
#from flask import url_for
#from werkzeug.utils import redirect

from forms.forms import loginForm
from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators
from wtforms.fields import EmailField, DateField

class UpdateAccount(Form):
    username = StringField('New Username: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('New Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('New Password: ', [validators.length(max=100), validators.DataRequired()])
    phone_number = StringField('New Phone Number: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    submit = SubmitField('Update')

#connect SQL to python
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

def validate_username(self, username):

    form = loginForm(csrf_enabled=False)
    user_email = form.email
    user_password = form.password
    staffEmail_Password = {}
    customerEmail_Password = {}

    # to execute SQL code for Staff email
    cursor = conn.cursor()
    cursor.execute('SELECT EmailAddr,Password from Staff')

    # to fetch result of the SQL code output for Staff's email
    cursor_data = cursor.fetchall()

    #change the Staff data format in dictionary form
    for i in cursor_data:
        staffEmail_Password.update( {i[0]:i[1]} )

    #905316862613659649> to execute SQL code for Customer's email
    cursor1 = conn.cursor()
    cursor1.execute('SELECT EmailAddr,Password from Customer')

    #905316862613659649> to fetch result of the SQL code output for Customer's email
    cursor1_data = cursor1.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor1_data:
        customerEmail_Password.update( {i[0]:i[1]} )
        #if username.data != current_user.username:
            #user = Users.query.filter_by(username=username.data).first()
            #pass
            #if user:
                #raise ValidationError('That username is taken. Please choose a different one.')

def validate_email(self, email):
    return signupValidation.validate_signUp_email()
