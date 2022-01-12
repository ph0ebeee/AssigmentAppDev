from dns import transaction
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash, session
# from flask_session import Session
import pyodbc
import shelve
import paypalrestsdk
#from flask_login import current_user, login_required

from products.SQLtoPython import products
from templates.paypal.receipt import Receipt
from werkzeug.utils import redirect
from forms import forms
#from flask_bcrypt import Bcrypt
from forms.forms import loginForm
from templates.staff import staff_forms
from templates.staff.staffcust import orders
from userAuthentication.loginValidation import *
from script import *

# from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm
from forms.forms import signupForm

app = Flask(__name__,template_folder="./templates")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
#bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('templates/paypal/success_payment.html')

#route for login form to be seen on loginPage.html  - viona
@app.route('/Login', methods=['GET', 'POST'])
def login():
    loginPage = loginForm()
    return render_template('usersLogin/loginPage.html', form=loginPage)

@app.route('/LoginValidate', methods=['GET', 'POST'])
def loginValidate():
    if request.method == 'POST':
        form = loginForm(request.form)
        validateCustLogin = validate_cust_login(form.email.data,form.password.data)
        validateStaffLogin = validate_staff_login(form.email.data,form.password.data)
        #use JS to change the layout of the navbar according to Cust or Staff account
        if validateCustLogin==True:
            custDetails = validated_Cust_Details(form.email.data,form.password.data)
            session['custID'] = (custDetails[0][0])
            session['custName'] = (custDetails[0][1])
            session['role'] = 'Customer'
            return render_template('customer/customerSettings.html', custDetails = custDetails)  # change to customer page
        elif validateStaffLogin == True:
            staffDetails = validated_Staff_Details(form.email.data,form.password.data)
            return render_template('usersLogin/loginPage.html', staffDetails = staffDetails)  # change to staff page
        # else:
        #     return render_template('usersLogin/loginPage.html', form=loginPage)

@app.route('/CustomerPurchase', methods=['GET', 'POST'])
def ViewCustPurchase():
    custPurchaseList = CustomerPurchase(session["custID"])
    return render_template('customer/customerPurchase.html', custPurchaseList = custPurchaseList)

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

@app.route('/AboutUs')   # added but havent push
def AboutUs():
    return render_template('about us/aboutUs.html')

@app.route('/DiscountedItems', methods=['GET', 'POST'])   # added but havent push
def DiscountedItems():
    to_send = products()
    return render_template('products/discountedItems.html', to_send=to_send)

@app.route('/TopSellingItems', methods=['GET', 'POST'])   # added but havent push
def TopSellingItems():
    to_send = products()
    return render_template('products/topSellingItems.html', to_send=to_send)

@app.route('/NewlyRestockedItems', methods=['GET', 'POST'])   # added but havent push
def NewlyRestockedItems():
    to_send = products()
    return render_template('products/newlyRestockedItems.html', to_send=to_send)

# chatbot done by Phoebe

# @app.route("/Chatbot", methods=['POST'])
# def chatbot():
#     text = request.get_json().get("message")
#     response = get_response(text)
#     message = {"answer": response}
#     return jsonify(message)

# payment via paypal done by Phoebe
# @app.route('/Success', methods = ['POST'])
# def send_receipt_info():
#     jsdata = request.form['javascript_data']
#     return jsdata

#Retrieve from sql to print receipt - Phoebe

# shopping cart by Phoebe
@app.route('/ShoppingCart/<int:id>', methods = ['POST'])
def update_items(id):
    cart_product= {}
    db = shelve.open('card_product.db','w')
    cart_product = db['Items']
    cart_product.insert(id)
    db['Items'] = cart_product
    db.close()


@app.route('/DeleteItems/<int:id>',methods =['POST'])                 #TEST
def delete_items(id):
    delete_items = {}
    db = shelve.open('cart_product.db', 'w')
    delete_items = db['Items']

    delete_items.pop(id)

    db['Items'] = delete_items
    db.close()

    return redirect(url_for('ShoppingCart'))


@app.route('/SuccessReceipt', methods =['GET'])
def retrieve_database_receipt():

    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    receipt_details ={}
    cursor = conn.cursor()
    cursor.execute('SELECT OrderID,POSDate,Totalprice from CustOrder')
    cursor_data = cursor.fetchall()
    return cursor_data

    # for i in cursor_data:
    #     receipt_details.update({i[0],i[1],i[2]})     # need to add the i[2]


def receipt_display():
    to_send = retrieve_database_receipt()
    return render_template("templates/paypal/success_payment.html", to_send=to_send)




# shopping cart by Phoebe

# @app.route('/ShoppingCart', methods = ['POST'])
# def add_product():
#     cart_product_name = {}
#@app.route('/ShoppingCart', methods = ['POST'])
#def add_product():
#    cart_product_name = {}





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

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')
# anna
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

@app.route('/acceptedOrder', methods=['GET', 'POST'])
def acceptedOrder():
    to_send= orders()
    return render_template('staff/accepted.html', to_send=to_send)

@app.route('/declinedOrder', methods=['GET', 'POST'])
def declinedOrder():
    to_send= orders()
    return render_template('staff/declined.html', to_send=to_send)

@app.route('/updateusername', methods=['GET', 'POST'])
def updateusername():
    UpdateStaff = staff_forms.UpdateAccount(csrf_enabled=False)
    if request.method == 'POST' and UpdateStaff.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according Staff account
    return render_template('staff/updateUsername.html', form=UpdateStaff)


if __name__ == '__main__':
    app.run()
