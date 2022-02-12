# from flask_session import Session
# from flask_login import current_user, login_required
import Feedback_class as Feedbacks
from templates.products.SQLtoPython import discounted_products, topselling_products, newlyrestocked_products, \
    household_products, frozen_products, grains_products
#from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, session, jsonify
# from flask_session import Session
#from products.SQLtoPython import products
from forms import forms
#from flask_bcrypt import Bcrypt
from forms.forms import updateCust, updateStaff,CreditCardForm, feedbackForm, createStaff, updateStaffaccount
from templates.staff.staffcust import StaffDetails, checkCust, checkStaff, checkOrder, checkProduct, checkManager, checkIntern, checkAss, updatestaff, updatecust, updatestaffsettings, \
    deletestaff, deletecust, createstaff, addpoints
from userAuthentication.loginValidation import *
from userAuthentication.signupValidation import *
from script import *
from templates.shoppingcart.arrangeMerge import array_merge
from datetime import datetime
from templates.paypal.CustomerInfo import CustomerInfo
from templates.paypal.receiptDetails import send_receipt_details
import shelve
from templates.chatbot.chat import get_response
from flask_cors import CORS
#from templates.Forms import CreateUserForm,CreateCustomerForm
from templates.shoppingcart.Shopping_cart import cart_items

app = Flask(__name__,template_folder="./templates")
app.secret_key = "secret key"
CORS(app)

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


@app.route('/staffHome')
#render staff.html template - anna
def staffhome():
    return render_template('./staff.html')


#route for login form to be seen on loginPage.html  - viona

# start of Viona's code 
#route for login form to be seen on loginPage.html
@app.route('/Login', methods=['GET', 'POST'])
def login():
    loginPage = loginForm()
    return render_template('usersLogin/loginPage.html', form=loginPage)

#route for sign up form to be seen on loginPage.html
@app.route('/Signup', methods=['GET', 'POST'])
def signUp():
    signUpPage = signupForm()
    return render_template('usersLogin/signupPage.html', form=signUpPage)

#validate users login details to respective customer / staff page
@app.route('/LoginValidate', methods=['GET', 'POST'])
def loginValidate():
    if request.method == 'POST':
        form = loginForm(request.form)
        validateCustLogin = validate_cust_login(form.email.data,form.password.data)
        validateStaffLogin = validate_staff_login(form.email.data,form.password.data)
        if validateCustLogin==True:
            custDetails = validated_Cust_Details(form.email.data)
            session['custID'] = (custDetails[0][0])
            session['custName'] = (custDetails[0][1])
            session['emailAddr'] = (custDetails[0][3])
            session['role'] = 'Customer'
            return redirect(url_for('custhome')) # change to customer page
        elif validateStaffLogin == True:
            staffDetails = validated_Staff_Details(form.email.data)
            session['staffID'] = (staffDetails[0][0])
            session['staffName'] = (staffDetails[0][1])
            session['emailAddr'] = (staffDetails[0][2])
            session['role'] = 'Staff'
            return render_template('./staff.html', staffDetails = staffDetails)  # change to staff page
        else:
            return redirect(url_for('login'))

#route for sign up form to be seen on signupPage.html
@app.route('/SignupCustomer',methods=['GET','POST'])
def registerCust():
    signupPage = forms.signupForm(csrf_enabled=False)
    if request.method == 'POST':
        form = signupForm(request.form)
        if (validate_signUp_email(form.email.data) == False):
            try:
                session['custID'] = create_new_customer(form.username.data,form.email.data, form.password.data,form.contactNum.data,form.address.data, form.postalCode.data) #conhtact num and postal code not in form
                session['role'] = 'Customer'
                print(session['custID'])
                return redirect(url_for('custhome'))
            except:
                errorMessage = "Failed to register"
                return render_template('usersLogin/signupPage.html',form=signupPage, errorMessage = errorMessage)
        else:
            errorMessage = "Email exists in database"
            return render_template('usersLogin/signupPage.html',form=signupPage, errorMessage = errorMessage) #if email exists in database, return back to sign up page
    return render_template('usersLogin/signupPage.html',form=signupPage)

#route for users to do change their password
@app.route('/ForgetPassword') 
def ForgetPassword():
    return render_template('forgetPassword.html')


#route to go customer's settings 
@app.route('/customerSettings', methods=['GET', 'POST'])
def ViewCustSettings():
    if (session['role'] == "Customer"):
        cust_details = CustDetails(session['custID'])
        return render_template('customer/customerSettings.html', cust_details = cust_details)
    else:
        return render_template('usersLogin/loginPage.html') 


#route to go purchase history in customer's settings
@app.route('/customerPurchase', methods=['GET', 'POST'])
def ViewCustPurchase():
    custPurchaseList = CustomerPurchase(session["custID"])
    return render_template('customer/customerPurchase.html', custPurchaseList = custPurchaseList)


#route to go available vouchers display page in customer's settings
@app.route('/customerVouchers', methods=['GET', 'POST'])
def ViewCustVouchers():
    custVoucherList = CustomerVoucher(session["custID"])
    dateNow = datetime.now()
    return render_template('customer/customerVouchers.html', custVoucherList = custVoucherList, dateNow=dateNow)


#route to go faq page in customer's settings
@app.route('/customerFAQ', methods=['GET', 'POST'])
def ViewFAQ():
    faqList = viewFAQ()
    return render_template('customer/customerFaq.html', faqList = faqList)


#route to go membership page in customer's settings
@app.route('/customerMembership', methods=['GET', 'POST'])
def ViewCustMembership():
    cust_details = CustDetails(session['custID'])
    return render_template('customer/customerMembership.html', cust_details = cust_details)


#route for staff website such that they are able to see the company's insights
@app.route('/inventory', methods=['GET', 'POST'])
def inventoryStats():
    oosList = checkOOS_items()
    topProductList = top_product()
    topProductList = topProductList[:10]
    topCustList = top_customer()
    topCustList = topCustList[:3]
    return render_template('staff/inventory.html', oosList = oosList, topProductList = topProductList, topCustList = topCustList)


@app.route('/AboutUs')   # added but havent push
def AboutUs():
    navbar="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
    return render_template('about_us/aboutUs.html', navbar = navbar)


# the contact_us form !
@app.route('/CreateContactUs', methods=['GET', 'POST'])
def create_contact_us():
    create_contact_form = feedbackForm(request.form)
    navbar="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
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
    return render_template('contact_us/contactUs.html', form=create_contact_form, navbar = navbar)


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

    return render_template('contact_us/RetrieveContact.html', count=len(contact_list), contact_list=contact_list)


@app.route('/Grains')
def grains_cat():
    to_send = grains_products() # loop
    # insert if else here using '.pop'
    # create another list to store wo yao de discounted items -> different,, go through the product list
    return render_template('products/grains.html', to_send=to_send)


@app.route('/Frozen')
def frozen_cat():
    to_send = frozen_products() # loop
    # insert if else here using '.pop'
    # create another list to store wo yao de discounted items -> different,, go through the product list
    return render_template('products/frozen.html', to_send=to_send)


@app.route('/Household')
def household_cat():
    to_send = household_products() # loop
    # insert if else here using '.pop'
    # create another list to store wo yao de discounted items -> different,, go through the product list
    return render_template('products/houseHold.html', to_send=to_send)


@app.route('/ShopCategories')   # added but havent push
def ShopCategories():
    navbar="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
    return render_template('products/shopCategories.html', navbar = navbar)


@app.route('/DiscountedItems', methods=['GET', 'POST'])   # added but havent push
def DiscountedItems():
    navbar="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
    to_send = discounted_products()
    # to_send = to_send[:5]
    return render_template('products/discountedItems.html', to_send=to_send, navbar = navbar)


@app.route('/TopSellingItems', methods=['GET', 'POST'])   # added but havent push
def TopSellingItems():
    navbar="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
    to_send = topselling_products()
    return render_template('products/topSellingItems.html', to_send=to_send, navbar = navbar)


@app.route('/NewlyRestockedItems', methods=['GET', 'POST'])   # added but havent push
def NewlyRestockedItems():
    navbar="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
    to_send = newlyrestocked_products() # loop
    # insert if else here using '.pop'
    # create another list to store wo yao de discounted items -> different,, go through the product list
    return render_template('products/newlyRestockedItems.html', to_send=to_send, navbar = navbar)


#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/StaffSettings', methods=['GET', 'POST'])
#staff account display - anna
def StaffSettings():
    if (session['role'] == "Staff"):
        staff_details = StaffDetails(session['staffID'])
        return render_template('staff/staff_account.html', staff_details = staff_details)
    else:
        return render_template('usersLogin/loginPage.html')


@app.route('/MainPage')
#staff home page return template - anna
def MainPage():
    return render_template('staff.html')


@app.route('/retrieveCustomers', methods=['GET', 'POST'])
#customer management retrieval - anna
def retrieve_customers():
    custList = checkCust()
    OrderList = checkOrder()
    productList = checkProduct()
    return render_template('staff/staff_cust.html', custList = custList, OrderList = OrderList, productList = productList)


@app.route('/retrieveStaff', methods=['GET', 'POST'])
#staff management retrieval - anna
def retrieve_staff():
    StaffList = checkStaff()
    ManagerList = checkManager()
    InternList = checkIntern()
    AssList = checkAss()
    return render_template('staff/retrieveStaff.html', StaffList = StaffList, ManagerList = ManagerList, InternList = InternList, AssList = AssList)


@app.route('/createStaff', methods=['GET', 'POST'])
#create staff, forms included - anna
def create_staff():
    create_staff_form = createStaff(request.form)
    if request.method == 'POST' and create_staff_form.validate():

        createstaff(create_staff_form.name.data,
                    create_staff_form.email.data,
                    create_staff_form.password.data,
                    create_staff_form.remarks.data)

        return redirect(url_for('retrieve_staff'))

    return render_template('staff/createStaff.html', form=create_staff_form)


@app.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
#update staff, forms included - anna
def update_staff(id):
    update_staff_form = updateStaff(request.form)
    if request.method == 'POST' and update_staff_form.validate():

        updatestaff(update_staff_form.name.data,
                    update_staff_form.email.data,
                    update_staff_form.remarks.data,
                    id)
        return redirect(url_for('retrieve_staff'))

    else:
        StaffList = StaffDetails(id)

        for i in StaffList:
            update_staff_form.name.data = StaffList[0][1]
            update_staff_form.email.data = StaffList[0][2]
            update_staff_form.remarks.data = StaffList[0][5]


        return render_template('staff/updateStaff.html', form=update_staff_form)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
#update customer details, forms included - anna
def update_user(id):
    update_user_form = updateCust(request.form)
    if request.method == 'POST' and update_user_form.validate():

        updatecust(update_user_form.name.data,
                    update_user_form.email.data,
                    update_user_form.membership.data,
                    update_user_form.contactNum.data,
                    update_user_form.address.data,
                    id)
        return redirect(url_for('retrieve_customers'))

    else:
        CustDetail = CustDetails(id)

        for i in CustDetail:
            update_user_form.name.data = CustDetail[0][1]
            update_user_form.email.data = CustDetail[0][3]
            update_user_form.membership.data = CustDetail[0][2]
            update_user_form.contactNum.data = CustDetail[0][6]
            update_user_form.address.data = CustDetail[0][7]


        return render_template('staff/updateUsers.html', form=update_user_form)


@app.route('/deleteUser/<int:id>', methods=['GET'])
#delete function for customer management - anna
def delete_user(id):
    deletecust(id)
    return redirect(url_for('retrieve_customers'))


@app.route('/deleteStaff/<int:id>', methods=['GET'])
#delete function for staff management - anna
def delete_staff(id):
    deletestaff(id)
    return redirect(url_for('retrieve_staff'))


@app.route('/updateStaffaccount/<int:id>/', methods=['GET', 'POST'])
#update staff account - username, email, password - anna
def update_staff_account(id):
    update_staff_account_form = updateStaffaccount(request.form)
    if request.method == 'POST' and update_staff_account_form.validate():

        updatestaffsettings(update_staff_account_form.name.data,
                    update_staff_account_form.email.data,
                    id)

        return redirect(url_for('StaffSettings'))

    else:
        StaffList = StaffDetails(id)

        for i in StaffList:
            update_staff_account_form.name.data = StaffList[0][1]
            update_staff_account_form.email.data = StaffList[0][2]

        return render_template('staff/updatesetting.html', form=update_staff_account_form)


@app.route('/game2')
#game 2 app route
def game2():
    return render_template('game2/game2.html')


@app.route('/aftergame2',methods=['POST'])
#adding of points 100 when victory
def claimpoints():
    addpoints(int(session['custID']))
    return render_template('game2/Reedem.html')


@app.route('/game2/redeem')
#render template for proof of victory and membership points earned
def redeem():
    return render_template('game2/Reedem.html')


# chatbot done by Phoebe


@app.route('/chatbot',methods=['POST'])
def predict():
    text = request.get_json().get('message')
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

# retrieve for receipt - phoebe


@app.route('/ReceiptDetails', methods =['POST'])
def receiptDetails():
    now = datetime.now()
    current_time = now.strftime("%d-%m-%Y %H:%M:%S")
    send_receipt_details('1', int(session['custID']), '2', current_time)
    return render_template('paypal/success_payment.html')


@app.route('/SuccessReceipt', methods =['GET','POST'])
def retrieve_database_receipt():
    try:
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'     
                              'Server=(localdb)\MSSQLLocalDB;'
                              'Database=EcoDen;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute('SELECT OrderID,TotalPrice,POSDate from CustOrder')
        cursor_data = cursor.fetchall()
        shopping_cart_dict = {}
        db = shelve.open('ShoppingCart.db', 'w')
        shopping_cart_dict = db['ShoppingCart']

        shopping_cart_dict.clear()

        db['ShoppingCart'] = shopping_cart_dict
        db.close()
        session.clear()
        return render_template("paypal/success_payment.html", to_send= cursor_data)
    except Exception as e:
        print(e)


# shopping cart - phoebe


@app.route('/ShoppingCart', methods = ['GET','POST'])           #product for testing
def open_cart():
    navbar ="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'     
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID,ProductName,ProductPrice from Product')
    cursor_data = cursor.fetchall()

    return render_template("shoppingcart/shopping_cart.html", to_send= cursor_data, navbar = navbar)


@app.route('/add', methods = ['POST'])
def add_product():
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        if _quantity and _code and request.method == 'POST':
            conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=(localdb)\MSSQLLocalDB;'
                              'Database=EcoDen;'
                              'Trusted_Connection=yes;')
            cursor = conn.cursor()
            cursor.execute('SELECT ProductID, ProductName, ProductPicture, ProductPrice from Product WHERE  ProductID = ?', _code)
            cursor_data = cursor.fetchone()
            selectedItem = { _code : {'name': cursor_data.ProductName, 'code': cursor_data.ProductID, 'image': cursor_data.ProductPicture, 'price' : cursor_data.ProductPrice, 'quantity' : _quantity, 'total_price': _quantity * cursor_data.ProductPrice}}
            print(selectedItem)
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
            shopping_cart_dict = {}
            db = shelve.open('ShoppingCart.db','c')

            try:
                shopping_cart_dict = db['ShoppingCart']

            except:
                print("Error in retrieving shopping cart from ShoppingCart.db")

            itemsSelect = cart_items(cursor_data.ProductID, cursor_data.ProductName, cursor_data.ProductPicture, cursor_data.ProductPrice, all_total_price,'','')
            shopping_cart_dict[itemsSelect.get_product_id()] = itemsSelect
            db['ShoppingCart'] = shopping_cart_dict
            db.close()

            return redirect(url_for('.open_cart'))

        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('open_cart'))


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
                        shopping_cart_dict = {}
                        db = shelve.open('ShoppingCart.db', 'w')
                        shopping_cart_dict = db['ShoppingCart']
                        shopping_cart_dict.pop(int(code))
                        db['ShoppingCart'] = shopping_cart_dict
                        db.close()

                break

        if all_total_quantity == 0:
            shopping_cart_dict = {}
            db = shelve.open('ShoppingCart.db', 'w')
            shopping_cart_dict = db['ShoppingCart']

            shopping_cart_dict.clear()

            db['ShoppingCart'] = shopping_cart_dict
            db.close()
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
        shopping_cart_dict = {}
        db = shelve.open('ShoppingCart.db', 'w')
        shopping_cart_dict = db['ShoppingCart']
        shopping_cart_dict.clear()

        db['ShoppingCart'] = shopping_cart_dict
        db.close()
        session.clear()
        return redirect(url_for('.open_cart'))
    except Exception as e:
        print(e)


@app.route('/PaymentCreditCard', methods=['GET', 'POST'])
def credit_card_form():
    CreditCard = CreditCardForm(request.form)
    shopping_list = []
    shopping_cart_dict = {}
    db = shelve.open('ShoppingCart.db', 'r')
    shopping_cart_dict = db['ShoppingCart']
    db.close()
    for key in shopping_cart_dict:
        cart = shopping_cart_dict.get(key)
        shopping_list.append(cart)
    if request.method == 'POST' and CreditCard.validate():
        customers_info_dict = {}
        db = shelve.open('customerInfo.db', 'c')

        try:
            customers_info_dict = db['CustomersInfo']
        except:
            print("Error in retrieving Customers Information from customerInfo.db.")

        customerInfo = CustomerInfo(CreditCard.name.data, CreditCard.email.data,  CreditCard.address.data, CreditCard.card_no.data, CreditCard.expiry.data, CreditCard.cvv.data)
        customers_info_dict[customerInfo.get_customer_id()] = customerInfo
        db['CustomersInfo'] = customers_info_dict

        db.close()

        return redirect(url_for('retrieve_database_receipt'))
    return render_template('paypal/customer_credit_form.html', form=CreditCard, shopping_list = shopping_list)



if __name__ == '__main__':
    app.run(debug=True)
