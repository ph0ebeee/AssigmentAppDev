from flask import Flask, render_template, request, session
# from flask_session import Session
#from products.SQLtoPython import products
from forms import forms
#from flask_bcrypt import Bcrypt
from forms.forms import CreateCustomerForm, CreateStaffForm
import users.Users as Users
from templates.staff import staff_forms
from userAuthentication.loginValidation import *
from script import *
import shelve, users
from templates.shoppingcart.arrangeMerge import array_merge
from datetime import datetime
import shelve, Staffs


# from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm

app = Flask(__name__,template_folder="./templates")
app.secret_key = "secret key"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
#bcrypt = Bcrypt(app)

@app.route('/')
#function for images selected to be seen on image slideshow  - viona
def home():
    image1 = './static/Assets/images/imageCarousel_1.jpg' 
    image2 = './static/Assets/images/imageCarousel_2.jpg' 
    image3 = './static/Assets/images/imageCarousel_3.jpg' 
    image4 = './static/Assets/images/imageCarousel_4.jpg' 
    image5 = './static/Assets/images/imageCarousel_5.jpg' 
    return render_template('./home.html',image1=image1,image2=image2,image3=image3,image4=image4,image5=image5)

@app.route('/custHome')
#function for images selected to be seen on image slideshow  - viona
def custhome():
    image1 = './static/Assets/images/imageCarousel_1.jpg' 
    image2 = './static/Assets/images/imageCarousel_2.jpg' 
    image3 = './static/Assets/images/imageCarousel_3.jpg' 
    image4 = './static/Assets/images/imageCarousel_4.jpg' 
    image5 = './static/Assets/images/imageCarousel_5.jpg' 
    return render_template('customer/home.html',image1=image1,image2=image2,image3=image3,image4=image4,image5=image5)

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
    if (session['role'] == "Customer"):
        cust_details = CustDetails(session['custID'])
        return render_template('customer/customerSettings.html', cust_details = cust_details)
    else:
        return render_template('usersLogin/loginPage.html') 

#route to go purchase history in customer's settings
@app.route('/CustomerPurchase', methods=['GET', 'POST'])
def ViewCustPurchase():
    custPurchaseList = CustomerPurchase(session["custID"])
    return render_template('customer/customerPurchase.html', custPurchaseList = custPurchaseList)

#route to go available vouchers display page in customer's settings
@app.route('/customerVouchers', methods=['GET', 'POST'])
def ViewCustVouchers():
    custVoucherList = CustomerVoucher(session["custID"])
    dateNow = datetime.now()
    return render_template('customer/customerVouchers.html', custVoucherList = custVoucherList, dateNow=dateNow)

#route to go available vouchers display page in customer's settings
@app.route('/customerFAQ', methods=['GET', 'POST'])
def ViewFAQ():
    faqList = viewFAQ()
    return render_template('customer/customerFaq.html', faqList = faqList)

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

@app.route('/custAboutUs')   # added but havent push
def custAboutUs():
    return render_template('customer/aboutUs.html')

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


@app.route('/SuccessReceipt', methods =['GET','POST'])
def retrieve_database_receipt():

    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'     
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT OrderID,POSDate,Totalprice from CustOrder')
    cursor_data = cursor.fetchall()
    return render_template("paypal/success_payment.html", to_send= cursor_data)




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

@app.route('/MainPage')
def MainPage():
    return render_template('staff.html')

@app.route('/createCustomers', methods=['GET', 'POST'])
def create_customers():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = Users.Users(create_customer_form.name.data,
                           create_customer_form.gender.data,
                           create_customer_form.email.data,
                           create_customer_form.address.data,
                           create_customer_form.membership.data,
                           create_customer_form.remarks.data)
        users_dict[user.get_id()] = user
        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('staff/staff_cust.html', form=create_customer_form)


@app.route('/retrieveCustomers')
def retrieve_customers():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)


    return render_template('staff/declined.html',count=len(users_list),users_list=users_list)

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_name(update_user_form.name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_email(update_user_form.email.data)
        user.set_address(update_user_form.address.data)
        user.set_membership(update_user_form.membership.data)
        user.set_remarks(update_user_form.remarks.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))

    else:
        users_dict = {}
        db = shelve.open('user.db','r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.name.data = user.get_first_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.email.data = user.get_email()
        update_user_form.address.data = user.get_address()
        update_user_form.membership.data = user.get_membership()
        update_user_form.remarks.data = user.get_remarks()

        return render_template('updateUsers.html', form=update_user_form)

@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'c')

        try:
            staff_dict = db['Staff']
        except:
            print("Error in retrieving Users from user.db.")

        staff = Users.Users(create_staff_form.name.data,
                           create_staff_form.email.data,
                           create_staff_form.address.data,
                           create_staff_form.role.data,
                           create_staff_form.remarks.data)
        staff_dict[staff.get_id()] = staff
        db['Staff'] = staff_dict
        db.close()

        return redirect(url_for('retrieve_staff'))
    return render_template('staff/createStaff.html', form=create_staff_form)


@app.route('/retrieveStaff')
def retrieve_staff():
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()

    staff_list = []
    for key in staff_dict:
        staff = staff_dict.get(key)
        staff_list.append(staff)


    return render_template('staff/retrieveStaff.html',count=len(staff_list),users_list=staff_list)

@app.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
def update_staff(id):
    update_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']

        staff = staff_dict.get(id)
        staff.set_name(update_staff_form.name.data)
        staff.set_email(update_staff_form.email.data)
        staff.set_address(update_staff_form.address.data)
        staff.set_membership(update_staff_form.role.data)
        staff.set_remarks(update_staff_form.remarks.data)

        db['Staff'] = staff_dict
        db.close()

        return redirect(url_for('retrieve_staff'))

    else:
        staff_dict = {}
        db = shelve.open('staff.db','r')
        staff_dict = db['Staff']
        db.close()

        staff = staff_dict.get(id)
        update_staff_form.name.data = staff.get_name()
        update_staff_form.email.data = staff.get_email()
        update_staff_form.address.data = staff.get_address()
        update_staff_form.role.data = staff.get_role()
        update_staff_form.remarks.data = staff.get_remarks()

        return render_template('updateStaff.html', form=update_staff_form)

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


#shopping cart - phoebe

@app.route('/ShoppingCart', methods = ['GET','POST'])           #product for testing
def open_cart():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'     
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID,ProductName,ProductPrice from Product')
    cursor_data = cursor.fetchall()
    return render_template("shoppingcart/shopping_cart.html", to_send= cursor_data)

@app.route('/ShoppingCart/add', methods = ['POST'])
def add_product():
    cursor = None
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        if _quantity and _code and request.method == 'POST':
            conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=(localdb)\MSSQLLocalDB;'
                              'Database=EcoDen;'
                              'Trusted_Connection=yes;')
            cursor = conn.cursor()
            cursor.execute('SELECT ProductID, ProductName, ProductPrice from Product WHERE  ProductID = ?', _code)
            cursor_data = cursor.fetchone()
            selectedItem = { _code : {'name' : cursor_data.ProductName, 'code' : cursor_data.ProductID, 'price' : cursor_data.ProductPrice, 'quantity' : _quantity, 'total_price': _quantity * cursor_data.ProductPrice}}
            all_total_price = 0
            all_total_quantity = 0

            session.modified = True
            if 'cart_item' in session:
                if cursor_data.ProductID in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if cursor_data.ProductID == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * cursor_data.ProductPrice
                else:
                    session['cart_item'] = array_merge(session['cart_item'], selectedItem)

                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = selectedItem
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * cursor_data.ProductPrice

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            return redirect(url_for('.open_cart'))

        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return redirect(url_for('.open_cart'))
    except Exception as e:
        print(e)


@app.route('/ShoppingCart/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.open_cart'))
    except Exception as e:
        print(e)



if __name__ == '__main__':
    app.run()
