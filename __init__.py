from flask import Flask, render_template, request, session
# from flask_session import Session
import shelve
# from flask_login import current_user, login_required
import Feedback_class as Feedbacks
from templates.products.SQLtoPython import discounted_products, topselling_products
from forms import forms
#from flask_bcrypt import Bcrypt
from templates.staff import staff_forms
from templates.staff.staffcust import orders
from userAuthentication.loginValidation import *
from script import *

from forms.forms import feedbackForm

# from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm

app = Flask(__name__,template_folder="./templates")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
#bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

#route for login form to be seen on loginPage.html  - viona
@app.route('/Login', methods=['GET', 'POST'])
def login():
    loginPage = loginForm()
    return render_template('usersLogin/loginPage.html', form=loginPage)

@app.route('/LoginValidate', methods=['GET', 'POST'])
def loginValidate(loginPage):
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
        else:
            return render_template('usersLogin/loginPage.html', form=loginPage)

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

@app.route('/AboutUs')
def AboutUs():
    return render_template('about_us/aboutUs.html')

# the contact_us form !
@app.route('/CreateContactUs', methods=['GET', 'POST'])
def create_contact_us():
    create_contact_form = feedbackForm(request.form)
    if request.method == 'POST' and create_contact_form.validate():
        contact_dict = {}
        db = shelve.open('contact.db', 'c')

        try:
            contact_dict = db['ContactUs']
        except:
            print("Error in retrieving Feedback from contact.db.")

        contact = Feedbacks.Feedback(create_contact_form.cust_name.data, create_contact_form.email.data, create_contact_form.feedback.data)
        contact_dict[contact.get_feedback_id()] = contact  # what is that for ?
        db['ContactUs'] = contact_dict

        # Test codes
        contact_dict = db['ContactUs']
        contact = contact_dict[contact.get_feedback_id()]
        print(contact.get_cust_name(), "was stored in contact.db successfully with feedback_id ==", contact.get_feedback_id)

        db.close()
        return redirect(url_for('home'))
    return render_template('contact_us/contactUs.html', form=create_contact_form)

@app.route('/RetrieveContactUs', methods=['GET', 'POST'])
def retrieve_contact_us():
    contact_dict = {}
    db = shelve.open('contact.db', 'r')
    contact_dict = db['ContactUs']
    db.close()

    contact_list = []
    for key in contact_dict:
        contact = contact_dict.get(key)
        contact_list.append(contact)

    return render_template('retrieveCustomers.html', count=len(contact_list), contact_list=contact_list)


@app.route('/ShopCategories')   # added but havent push
def ShopCategories():
    return render_template('products/shopCategories.html')

@app.route('/DiscountedItems', methods=['GET', 'POST'])   # added but havent push
def DiscountedItems():
    to_send = discounted_products()
    # to_send = to_send[:5]
    return render_template('products/discountedItems.html', to_send=to_send)

@app.route('/TopSellingItems', methods=['GET', 'POST'])   # added but havent push
def TopSellingItems():
    to_send = topselling_products()
    return render_template('products/topSellingItems.html', to_send=to_send)

@app.route('/NewlyRestockedItems', methods=['GET', 'POST'])   # added but havent push
def NewlyRestockedItems():
    to_send = discounted_products() # loop
    # insert if else here using '.pop'
    # create another list to store wo yao de discounted items -> different,, go through the product list
    return render_template('products/newlyRestockedItems.html', to_send=to_send)

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
    return render_template('success_payment.html')

# shopping cart by Phoebe
@app.route('/ShoppingCart', methods = ['POST'])
def add_product():
    cart_product_name = {}

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
    for i in cursor_data:
        receipt_details.update({i[0],i[1],i[2]})     # need to add the i[2]




# shopping cart by Phoebe

# @app.route('/ShoppingCart', methods = ['POST'])
# def add_product():
#     cart_product_name = {}

#@app.route('/ShoppingCart', methods = ['POST'])
#def add_product():
#    cart_product_name = {}


@app.route('/DeleteItems/<int:id>',methods =['POST'])                 #change the int:id
def delete_items(id):
    delete_items = {}
    db = shelve.open('cart_product.db', 'w')
    delete_items = db['Items']

    delete_items.pop(id)

    db['Items'] = delete_items
    db.close()

    return redirect(url_for('#'))  #figure out what is meant to be at the hashtag




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
