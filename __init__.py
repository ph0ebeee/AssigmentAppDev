from dns import transaction
from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
import pyodbc
import shelve
import paypalrestsdk
from flask_login import current_user, login_required
from templates.paypal.receipt import Receipt
from werkzeug.utils import redirect
from forms import forms
from flask_bcrypt import Bcrypt
from forms.forms import loginForm
from templates.staff import staff_forms
from templates.staff.staffcust import orders
from userAuthentication.loginValidation import *

# from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm
from forms.forms import signupForm

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

#route for login form to be seen on loginPage.html  - viona
@app.route('/Login', methods=['GET', 'POST'])
def login():
    loginPage = forms.loginForm(csrf_enabled=False)
    if request.method == 'POST' and loginPage.validate() == True :
        validateCustLogin = validate_cust_login()
        validateStaffLogin = validate_staff_login()
        #use JS to change the layout of the navbar according to Cust or Staff account
        if validateCustLogin==True:
            custDetails = validated_Cust_Details()
            return render_template('customer/customerSettings.html', custDetails = custDetails)  # change to customer page
        elif validateStaffLogin == True:
            staffDetails = validated_Staff_Details()
            return render_template('usersLogin/loginPage.html', staffDetails = staffDetails)  # change to staff page
        else:
            return render_template('usersLogin/loginPage.html', form=loginPage)
    else:
        return render_template('usersLogin/loginPage.html', form=loginPage)

#route for sign up form to be seen on loginPage.html  - viona
@app.route('/Signup',methods=['GET','POST'])
def signUp():
    signupPage = forms.signupForm(csrf_enabled=False)
    if request.method == 'POST' and signupPage.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according to Cust or Staff account
    return render_template('signupPage.html', form=signupPage)

@app.route('/ForgetPassword')
def ForgetPassword():
    return render_template('forgetPassword.html')

@app.route('/AboutUs')
def AboutUs():
    return render_template('about us/aboutUs.html')

# chatbot done by Phoebe

# @app.route("/Chatbot", methods=['POST'])
# def chatbot():
#     text = request.get_json().get("message")
#     response = get_response(text)
#     message = {"answer": response}
#     return jsonify(message)

# payment via paypal done by Phoebe
@app.route('/Payment', methods=['POST'])
def payment():
    return render_template('paypal_standard.html')

@app.route('/Success', methods = ['POST'])
def send_receipt_info():
    jsdata = request.form['javascript_data']
    return jsdata

#Retrieve from sql to print receipt - Phoebe
@app.route('/Payment/Success', methods = ['POST'])
def success_payment():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    receipt_details ={}
    cursor = conn.cursor()
    cursor.execute('SELECT OrderID,POSDate,Totalprice from CustOrder')
    cursor_data = cursor.fetchall()
    for i in cursor_data:
        receipt_details.update({i[0],i[1],i[2]})     # need to add the i[2]




# shopping cart by Phoebe
@app.route('/ShoppingCart', methods = ['POST'])
def add_product():
    cart_product_name = {}

@app.route('/DeleteItems/<int:id>',methods =['POST'])                 #change the int:id
def delete_items(id):
    delete_items = {}
    db = shelve.open('cart_product.db', 'w')
    delete_items = db['Items']

    delete_items.pop(id)

    db['Items'] = delete_items
    db.close()

    return redirect(url_for('#'))  #figure out what is meant to be at the hashtag





# @app.route('/contactUs', methods=['GET', 'POST'])
# def feedback():
#     feedback = CreateUserForm(request.form)
#     if request.method == 'POST' and feedback.validate():
#         users_dict = {}
#         db = shelve.open('user.db', 'c')
#
#         try:
#             users_dict = db['Users']
#         except:
#             print("Error in retrieving Users from user.db.")
#
#         user = User.User(feedback.name.data, feedback.response.data)
#         users_dict[user.get_user_id()] = user
#         db['Users'] = users_dict

# anna
#@app.route('/logout')
#def logout():
 #   logout_user()
 #   return render_template('home.html')

@app.route('/staffaccount', methods=['GET', 'POST'])
def staffaccount():
    UpdateStaff = staff_forms.UpdateAccount(csrf_enabled=False)
    if request.method == 'POST' and UpdateStaff.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according Staff account
    return render_template('staff/staff_account.html', form=UpdateStaff)

@app.route('/customerManagement', methods=['GET', 'POST'])
def customerManagement():
    to_send= orders()
    return render_template("staff/staff_cust.html", to_send=to_send)

@app.route('/acceptedOrder')
def acceptedOrder():
    return render_template('staff/accepted.html')

@app.route('/declinedOrder')
def declinedOrder():
    return render_template('staff/declined.html')

@app.route('/updateusername', methods=['GET', 'POST'])
def updateusername():
    UpdateStaff = staff_forms.UpdateAccount(csrf_enabled=False)
    if request.method == 'POST' and UpdateStaff.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according Staff account
    return render_template('staff/updateUsername.html', form=UpdateStaff)

if __name__ == '__main__':
    app.run()
