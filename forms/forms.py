from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators, RadioField, IntegerField
from wtforms.fields import EmailField, DateField


class signupForm(Form):
    username = StringField('Username:', [validators.Length(min=1, max=150), validators.DataRequired()])
    first_name = StringField('First Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender:', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email:', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:', [validators.length(max=100), validators.DataRequired()])
    address = TextAreaField('Mailing Address:', [validators.length(max=200), validators.DataRequired()])


class loginForm(Form):
    email = EmailField('Email:', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:', [validators.length(max=100), validators.DataRequired()])


class feedbackForm(Form):
    cust_name = StringField('Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email:', [validators.Email(), validators.DataRequired()])
    feedback = StringField('FeedBack:', [validators.Length(min=1, max=150), validators.DataRequired()])


class createProduct(Form):
    product_Name = StringField('Product Name: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_Category = StringField('Product Category: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_Price = StringField('Product Price: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_Desc = StringField('Product Description: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_Stock = StringField('Product StockCount: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_Discount = StringField('Discount Rate of Product: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_Date = StringField('Date of Product Update : ', [validators.Length(min=1, max=150), validators.DataRequired()])


class updateCust(Form):
    name = StringField('Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email:', [validators.Email(), validators.DataRequired()])
    address = TextAreaField('Mailing Address:', [validators.length(max=200), validators.DataRequired()])
    contactNum = TextAreaField('Contact Number:', [validators.length(max=200), validators.DataRequired()])
    membership = TextAreaField('Membership Points:', [validators.length(max=200), validators.DataRequired()])

class updateStaff(Form):
    name = StringField('Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email:', [validators.Email(), validators.DataRequired()])

class createStaff(Form):
    name = StringField('Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email:', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:', [validators.length(max=100), validators.DataRequired()])

class CreditCardForm(Form):
    name = StringField('Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = TextAreaField('Mailing Address:', [validators.length(max=200), validators.DataRequired()])
    card_no = IntegerField('Card Number:', [validators.Length(min=16, max=16), validators.DataRequired()])
    expiry = DateField('Valid Till:', [validators.Length(min=1, max=150), validators.DataRequired()])
    cvc = IntegerField('CVC:', [validators.Length(min=3, max=3), validators.DataRequired()])

