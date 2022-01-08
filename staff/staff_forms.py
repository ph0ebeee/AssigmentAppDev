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

#connect SQL to python
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):

        form = loginForm(csrf_enabled=False)
        user_email = form.email
        user_password = form.password
        staffEmail_Password = {}
        customerEmail_Password = {}

        #code to execute SQL code for Staff email
        cursor = conn.cursor()
        cursor.execute('SELECT EmailAddr,Password from Staff')

        #code to fetch result of the SQL code output for Staff's email
        cursor_data = cursor.fetchall()

        #change the Staff data format in dictionary form
        for i in cursor_data:
            staffEmail_Password.update( {i[0]:i[1]} )

        #code to execute SQL code for Customer's email
        cursor1 = conn.cursor()
        cursor1.execute('SELECT EmailAddr,Password from Customer')

        #code to fetch result of the SQL code output for Customer's email
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
