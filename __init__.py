from flask import Flask, render_template, request, session
# from flask_session import Session
from products.SQLtoPython import products
from forms import forms
#from flask_bcrypt import Bcrypt
from forms.forms import createCust
from templates.staff import staff_forms
from userAuthentication.loginValidation import *
from script import *
import shelve, users
from shoppingcart.cartdu import add_product_to_cart, empty_cart, backproduct

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

#validate users login details to respective customer / staff page
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
            session['emailAddr'] = (custDetails[0][3])
            session['role'] = 'Customer'
            return render_template('customer/customerPage.html') # change to customer page
        elif validateStaffLogin == True:
            staffDetails = validated_Staff_Details(form.email.data,form.password.data)
            return render_template('usersLogin/loginPage.html', staffDetails = staffDetails)  # change to staff page
        #else:
            # return render_template('usersLogin/loginPage.html', form=loginPage)

#route to go customer's settings 
@app.route('/CustomerSettings', methods=['GET', 'POST'])
def ViewCustSettings():
    cust_details = CustDetails(session['custID'])
    return render_template('customer/customerSettings.html', cust_details = cust_details)

#route to go purchase history in customer's settings
@app.route('/CustomerPurchase', methods=['GET', 'POST'])
def ViewCustPurchase():
    custPurchaseList = CustomerPurchase(session["custID"])
    return render_template('customer/customerPurchase.html', custPurchaseList = custPurchaseList)

#route for sign up form to be seen on loginPage.html viona: TBC
@app.route('/Signup',methods=['GET','POST'])
def signUp():
    signupPage = forms.signupForm(csrf_enabled=False)
    if request.method == 'POST' and signupPage.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according to Cust or Staff account
    return render_template('signupPage.html', form=signupPage)

@app.route('/ForgetPassword') #viona: TBC
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

# shoppingcart by Phoebe
@app.route('/ShoppingCart/<int:id>', methods = ['POST'])
def update_items(id):
    cart_product = {}
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

@app.route('/ShoppingCart', methods = ['GET','POST'])
def open_cart():
    add_product_to_cart()
    empty_cart()
    backproduct()
    return render_template("shoppingcart/shopping_cart.html")

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
    return render_template("paypal/success_payment.html", to_send=to_send)

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

# anna's staff logout
#@app.route('/logout')
#def logout():
    # This code is to hide the main tkinter window
    #root = tkinter.Tk()
    #root.withdraw()
    # Message Box
    #messagebox.showinfo("Title", "Message")
    #root.destroy()

    #return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')


@app.route('/staffaccount', methods=['GET', 'POST'])
def staffaccount():
    UpdateStaff = staff_forms.UpdateAccount(csrf_enabled=False)
    if request.method == 'POST' and UpdateStaff.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according Staff account
    return render_template('staff/staff_account.html', form=UpdateStaff)


@app.route('/customerManagement', methods=['GET', 'POST'])
def customerManagement():
    create_customer_form = createCust(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = users.Users(create_customer_form.first_name.data, create_customer_form.last_name.data, create_customer_form.gender.data, create_customer_form.email.data, create_customer_form.address.data, create_customer_form.membership.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==", user.get_user_id())


        return redirect(url_for('retrieveUsers'))
    return render_template('staff/staff_cust.html', form=create_customer_form)


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)


    return render_template('staff/declined.html')

#@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
#def update_user(id):
    #update_customer_form = createCust(request.form)

   #return render_template('updatecustomer.html', form=update_customer_form)


@app.route('/updateusername', methods=['GET', 'POST'])
def updateusername():
    UpdateStaff = staff_forms.UpdateAccount(csrf_enabled=False)
    if request.method == 'POST' and UpdateStaff.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according Staff account
    return render_template('staff/updateUsername.html', form=UpdateStaff)


@app.route('/game2')
def game2():
    return render_template('game2/game2.html')


if __name__ == '__main__':
    app.run()
