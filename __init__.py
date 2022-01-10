from dns import transaction
from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
import pyodbc
import shelve
import paypalrestsdk
from templates.paypal.receipt import Receipt
from werkzeug.utils import redirect
from forms import forms
#from flask_bcrypt import Bcrypt
from forms.forms import loginForm
from templates.staff import staff_forms
from userAuthentication.loginValidation import *

# from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm
from forms.forms import signupForm

app = Flask(__name__)
#bcrypt = Bcrypt(app)

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
#

# payment via paypal done by Phoebe
@app.route('/Payment', methods=['POST'])
def payment():
    return render_template('paypal_standard.html')

@app.route('/Success', methods = ['POST'])
def send_receipt_info():
    jsdata = request.form['javascript_data']
    return jsdata

<<<<<<< HEAD
@app.route('/Payment/Success', methods = ['POST'])
def success_payment():
    return render_template('success_payment.html')

# shopping cart by Phoebe
@app.route('/ShoppingCart', methods = ['POST'])
def add_product():
    cart_product_name = {}
=======
@app.route('/SuccessReceipt', methods =['GET'])
def retrieve_database_receipt():
>>>>>>> e473bdc275dc420dc333911e365451df999a8ed3
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT trans_num,time,total from transactionTable')
    cursor_data = cursor.fetchall()
    return cursor_data
def success_payment():
    to_send= retrieve_database_receipt()
    return render_template("success_payment", to_send=to_send)


# shopping cart by Phoebe
# @app.route("/ShoppingCart",methods = ["GET"])
# def shopping_cart():
#     return render_template('shopping cart/shopping_cart.html')
#

<<<<<<< HEAD
=======
# @app.route('/ShoppingCart', methods = ['POST'])
# def add_product():
#     cart_product = {}
#     db = shelve.open(cart_product)
#
#     try:
#         cart_product = db['Products']
#     except:
#         print("Error in retrieving Products from products.db")
#
#     conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                       'Server=(localdb)\MSSQLLocalDB;'
#                       'Database=EcoDen;'
#                       'Trusted_Connection=yes;')
#     cursor = conn.cursor()
#     cursor.execute('SELECT ProductName from Product')
#     cursor_data = cursor.fetchall()
#     for i in cursor_data:
#         cart_product.update( {i[0]:i[1]} )
#
# @app.route('/deleteProduct', methods = ['POST'])
# def delete_product():
#     pass

# @app.route('/add', methods=['POST'])
# def add_product_to_cart():
# 	try:
#             conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                               'Server=(localdb)\MSSQLLocalDB;'
#                               'Database=EcoDen;'
#                               'Trusted_Connection=yes;')
#             cart_product = {}
#             cursor = conn.cursor()
#             cursor.execute('SELECT ProductName from Product')
#             cursor_data = cursor.fetchone()
#             for i in cursor_data:
#                 cart_product.update({i[0]:i[1]}) #change the array to the suitable variable
#                 all_total_price = 0
#                 all_total_quantity = 0
#
#                 for key, value in session['cart_item'].items():
#                     if cursor_data['code'] == key:
#                         #session.modified = True
#                         #if session['cart_item'][key]['quantity'] is not None:
#                         #	session['cart_item'][key]['quantity'] = 0
#                         old_quantity = ['cart_item'][key]['quantity']
#                         total_quantity = old_quantity + _quantity
#                         ['cart_item'][key]['quantity'] = total_quantity
#                         ['cart_item'][key]['total_price'] = total_quantity * cursor_data['price']
# 				else:
# 					['cart_item'] = array_merge(session['cart_item'], itemArray)
#
# 				for key, value in session['cart_item'].items():
# 					individual_quantity = int(session['cart_item'][key]['quantity'])
# 					individual_price = float(session['cart_item'][key]['total_price'])
# 					all_total_quantity = all_total_quantity + individual_quantity
# 					all_total_price = all_total_price + individual_price
# 			else:
# 				session['cart_item'] = itemArray
# 				all_total_quantity = all_total_quantity + _quantity
# 				all_total_price = all_total_price + _quantity * cursor_data['price']
#
# 			session['all_total_quantity'] = all_total_quantity
# 			session['all_total_price'] = all_total_price
#
# 			return redirect(url_for('.products'))
# 		else:
# 			return 'Error while adding item to cart'
#     finally:
#         pass
#
# @app.route('/')
# def products():
# 	try:
#             conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                               'Server=(localdb)\MSSQLLocalDB;'
#                               'Database=EcoDen;'
#                               'Trusted_Connection=yes;')
#             cart_product = {}
#             cursor = conn.cursor()
#             cursor.execute('SELECT ProductName from Product')
#             cursor_data = cursor.fetchall()
#             for i in cursor_data:
#                 cart_product.update({i[0]:i[1]}) #change the array to the suitable variable
#             return render_template('products.html', products=cursor_data)
# 	finally:
# 		cursor.close()
# 		conn.close()
#
#
# @app.route('/delete')
# def delete_product():
# 	try:
# 		all_total_price = 0
# 		all_total_quantity = 0
#                 for key, value in ['cart_item'].items():
#                     individual_quantity = int(['cart_item'][key]['quantity'])
#                     individual_price = float(['cart_item'][key]['total_price'])
#                     all_total_quantity = all_total_quantity + individual_quantity
#                     all_total_price = all_total_price + individual_price
#
# 		# if all_total_quantity == 0:
# 		# 	session.clear()
# 		# else:
# 		# 	session['all_total_quantity'] = all_total_quantity             WORK ON THESE!!!
# 		# 	session['all_total_price'] = all_total_price
#
# 		# return redirect('/')
# 		return redirect(url_for('.products'))
#     finally:
#         pass
#
# def array_merge( first_array , second_array ):
# 	if isinstance( first_array , list ) and isinstance( second_array , list ):
# 		return first_array + second_array
# 	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
# 		return dict( list( first_array.items() ) + list( second_array.items() ) )
# 	elif isinstance( first_array , set ) and isinstance( second_array , set ):
# 		return first_array.union( second_array )
# 	return False
#
#

>>>>>>> e473bdc275dc420dc333911e365451df999a8ed3
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

<<<<<<< HEAD
=======
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

>>>>>>> e473bdc275dc420dc333911e365451df999a8ed3
if __name__ == '__main__':
    app.run()
