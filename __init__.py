# from flask_session import Session
# from flask_login import current_user, login_required
import Feedback_class as Feedbacks
from templates.products.SQLtoPython import discounted_products, topselling_products, newlyrestocked_products, \
    household_products, frozen_products, grains_products, create_products, update_products, ProductDetails, \
    all_products, delete_products
#from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, session, jsonify, flash
# from flask_session import Session
#from products.SQLtoPython import products
from forms import forms
import jwt
#from flask_bcrypt import Bcrypt
from forms.forms import updateCust, updateStaff, CreditCardForm, feedbackForm, createStaff, updateStaffaccount, \
    createProduct, updateProduct
from templates.staff.staffcust import StaffDetails, checkCust, checkStaff, checkOrder, checkProduct, checkManager, \
    checkIntern, checkAss, updatestaff, updatecust, updatestaffsettings, \
    deletestaff, deletecust, createstaff, addpoints, deductpoints
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
import secrets
#from templates.Forms import CreateUserForm,CreateCustomerForm
from templates.shoppingcart.Shopping_cart import cart_items
from threading import Thread
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager

app = Flask(__name__,template_folder="./templates")
app.secret_key = "secret key"
CORS(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "homeden123@gmail.com"
app.config['MAIL_PASSWORD'] = "appDevAssignment123"
jwt = JWTManager(app)
# Session(app)
#bcrypt = Bcrypt(app)


@app.route('/')
#function for images selected to be seen on image slideshow  - viona
def home():
    image1 = './static/Assets/images/staff_working.png'
    image2 = './static/Assets/images/eggs.png'
    image4 = './static/Assets/images/game2.png'
    image5 = './static/Assets/images/voucher.png'
    return render_template('./home.html',image1=image1,image2=image2,image4=image4,image5=image5)


@app.route('/custHome')
#function for images selected to be seen on image slideshow  - viona
def custhome():
    image1 = './static/Assets/images/staff_working.png'
    image2 = './static/Assets/images/eggs.png'
    image4 = './static/Assets/images/game2.png'
    image5 = './static/Assets/images/voucher.png'
    return render_template('customer/home.html',image1=image1,image2=image2,image4=image4,image5=image5)


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
                custDetails = validated_Cust_Details(form.email.data)
                session['custName'] = (custDetails[0][1])
                session['emailAddr'] = (custDetails[0][3])
                session['role'] = 'Customer'
                return redirect(url_for('custhome'))
            except:
                errorMessage = "Failed to register"
                return render_template('usersLogin/signupPage.html',form=signupPage, errorMessage = errorMessage)
        else:
            errorMessage = "Email exists in database"
            return render_template('usersLogin/signupPage.html',form=signupPage, errorMessage = errorMessage) #if email exists in database, return back to sign up page
    return render_template('usersLogin/signupPage.html',form=signupPage)

#route for users to do change their password
@app.route('/ForgetPassword',methods=['GET','POST'])
def ForgetPassword():
    emailForm = forms.emailForm(csrf_enabled=False)
    message = "Email will only be sent if you have an account!"
    return render_template('forgetPassword/send_resetLink_form.html', form = emailForm,message = message)

#route for users to do change their password
@app.route('/reset_password',methods=['GET','POST'])
def sendForgetEmail():
    emailForm = forms.emailForm(csrf_enabled=False)
    if request.method == 'POST':
        form = forms.emailForm(request.form)
        message = "Email will only be sent if you have an account!"
        if form.validate():
            email = form.email.data
            if validated_Cust_Exists(email) == True:
                salt = CustPwSalt_byEmail(email)
                cust_id = getCustId(email)
                send_password_reset_link(email,cust_id, salt, app, cust_id)
                message = "Email has been sent! Please check your Gmail Inbox"
                return render_template('forgetPassword/send_resetLink_form.html', form = emailForm, message = message)
            else:
                message = "Account associated with Email entered not found"
                return render_template('forgetPassword/send_resetLink_form.html', form = emailForm, message = message)
        else:
            return render_template('forgetPassword/send_resetLink_form.html', form = emailForm, message = message) #if email exists in database, return back to sign up page

    return render_template('forgetPassword/send_resetLink_form.html', form = emailForm)

@app.route("/reset_password/<token>/<int:user_id>", methods=['GET','POST'])
def reset_token(token, user_id):
    form = forms.passwordForm()
    #try:
    reset_token = token
    user_id = user_id

    if request.method == 'POST':
        Passwordform = forms.passwordForm(request.form)
        salt = CustPwSalt_byID(user_id)
        passwordEncode = Passwordform.password.data.encode("utf-8")
        passwordSalt = salt.encode("utf-8")
        hashedPw = bcrypt.hashpw(passwordEncode, passwordSalt)
        hashedPw = hashedPw.decode('UTF-8')
        updatePassword(user_id, hashedPw)
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('forgetPassword/reset_password_form.html', form=form)

    return render_template('forgetPassword/reset_password_form.html', form = form)
    #except:
    #    flash('The password reset link is invalid or has expired.', 'error')
    #    return redirect(url_for('login'))

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


#viona :route for staff website such that they are able to see the company's insights
@app.route('/inventory', methods=['GET', 'POST'])
def inventoryStats():
    #data tables
    oosList = checkOOS_items()
    topProductList = top_product()
    topProductList = topProductList[:10]
    topCustList = top_customer()
    topCustList = topCustList[:3] #only select top 3
    monthList = [1,2,3,4,5,6,7,8,9,10,11,12]  #drop down list
    yearList = [2021,2022] #drop down list
    revenue_year = request.form.get("revYear")
    if revenue_year == None:
        revenue_year = 2021

    cat_year = request.form.get("catYear")
    if cat_year == None:
        cat_year = 2021

    cat_month = request.form.get("catMonth")
    if cat_month == None:
        cat_month = 11
    #lists of data
    revenue = RetrieveMonthlyOverallSalesRevenue(revenue_year)
    topCategories = RetrieveTopSellingProductCategory(cat_month,cat_year)
    topCategories = topCategories[:5] #only select top 3
    #to plot graph
    MonthlyRevenuelabel = [row[0] for row in revenue]
    MonthlyRevenuevalues = [float(row[1]) for row in revenue]

    topCatlabel = [row[0] for row in topCategories]
    topCatvalues = [float(row[1]) for row in topCategories]
    return render_template('staff/inventory.html', oosList = oosList, topProductList = topProductList, topCustList = topCustList,monthList=monthList,yearList=yearList,MonthlyRevenuelabel=MonthlyRevenuelabel, MonthlyRevenuevalues=MonthlyRevenuevalues, topCatlabel=topCatlabel, topCatvalues=topCatvalues,revenue_year=revenue_year,cat_year=cat_year,cat_month=cat_month)

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

@app.route('/CreateProducts', methods=['GET', 'POST'])
def create_product():
    create_product_form = createProduct(request.form)
    if request.method == 'POST' and create_product_form.validate():

        create_products(create_product_form.product_Category.data,
                    create_product_form.product_Picture.data,
                    create_product_form.product_Name.data,
                    create_product_form.product_Desc.data,
                    float(create_product_form.product_Price.data), # float 2dp
                    int(create_product_form.product_Stock.data),
                    float(create_product_form.product_Discount.data),
                    create_product_form.product_Date.data)

    return render_template('products/createProduct.html', form=create_product_form)

@app.route('/UpdateProducts/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = updateProduct(request.form)
    if request.method == 'POST' and update_product_form.validate():

        update_products(update_product_form.product_Category.data,
                    update_product_form.product_Picture.data,
                    update_product_form.product_Name.data,
                    update_product_form.product_Desc.data,
                    float(update_product_form.product_Price.data),
                    int(update_product_form.product_Stock.data),
                    float(update_product_form.product_Discount.data),
                    update_product_form.product_Date.data,id)

        return redirect(url_for('retrieve_product'))

    else:
            ProductList = ProductDetails(id)

            for i in ProductList:
                update_product_form.product_Category.data = ProductList[0][2]
                update_product_form.product_Picture.data = ProductList[0][1]
                update_product_form.product_Name.data = ProductList[0][3]
                update_product_form.product_Desc.data = ProductList[0][4]
                update_product_form.product_Price.data = ProductList[0][5]
                update_product_form.product_Stock.data = ProductList[0][6]
                update_product_form.product_Discount.data = ProductList[0][7]
                update_product_form.product_Date.data = ProductList[0][8]


    return render_template('products/updateProduct.html', form=update_product_form)

@app.route('/RetrieveProducts', methods=['GET', 'POST'])
def retrieve_product():
    ProductList = all_products()
    return render_template('products/retrieveProduct.html', ProductList = ProductList)

@app.route('/DeleteProducts/<int:id>', methods=['GET'])
def delete_productt(id):    # mis-spelled on purpose
    delete_products(id)
    return redirect(url_for('retrieve_product'))

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
                    #update_staff_account_form.password.data,
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


@app.route('/ReceiptDetails', methods =['GET','POST'])
def receiptDetails():
    try:
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                              'Server=(localdb)\MSSQLLocalDB;'
                              'Database=EcoDen;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute('SELECT max(OrderID) FROM CustOrder')
        cursor_data = cursor.fetchval()
        order_id = int(cursor_data) + 1
        now = datetime.now()
        current_time = now.strftime("%d-%b-%y %H:%M:%S")
        if request.method == 'POST':
            price = request.form['totalprice']
            send_receipt_details('3',price, current_time,order_id)
            if 'cart_item' in session:
                session.pop('cart_item')
            return redirect(url_for(retrieve_database_receipt))

    except Exception as e:
        print('prob is',e)
        return redirect(url_for('.login'))


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
        if 'cart_item' in session:
            session.pop('cart_item')

        return render_template("paypal/success_payment.html", to_send= cursor_data)
    except Exception as e:
        print(e)


# shopping cart - phoebe


@app.route('/ShoppingCart', methods = ['GET','POST'])           #product for testing
def open_cart():
    navbar="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_nobot.html"
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'     
                              'Server=(localdb)\MSSQLLocalDB;'
                              'Database=EcoDen;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute('SELECT ProductID,ProductName,ProductPrice from Product')
        cursor_data = cursor.fetchall()

        return render_template("shoppingcart/shopping_cart.html", to_send= cursor_data, navbar = navbar)
    return render_template('errorpage.html', navbar = navbar)



@app.route('/add', methods = ['POST'])
def add_product():
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_customer.html"
    else:
        return redirect(url_for('login'))
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

            all_total_price = "{:.2f}".format(all_total_price)
            itemsSelect = cart_items(cursor_data.ProductID, cursor_data.ProductName, cursor_data.ProductPicture, cursor_data.ProductPrice, all_total_price,'','')
            shopping_cart_dict[itemsSelect.get_product_id()] = itemsSelect
            db['ShoppingCart'] = shopping_cart_dict
            db.close()

            return redirect(url_for('.open_cart'))

        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
        return render_template('errorpage')
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
                        price = cart_items(int(code),'','','',all_total_price,'','')
                        shopping_cart_dict[price.get_product_id()] = price

                        # dictionary = shopping_cart_dict
                        # new_total = dictionary.get_price()

                        for key,value in shopping_cart_dict.items():
                            print(key,value)

                        # print(new_total)
                        # shopping_cart_dict.update(new_total)

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
            if 'cart_item' in session:
                session.pop('cart_item')
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
        if 'cart_item' in session:
            session.pop('cart_item')
        return redirect(url_for('.open_cart'))
    except Exception as e:
        print(e)


@app.route('/PaymentCreditCard', methods=['GET', 'POST'])
def credit_card_form():
    cust_details = CustDetails(session['custID'])
    deductpoints(int(session['custID']))
    navbar ="base.html"
    role = session.get('role')
    if (role == 'Staff'):
        navbar = "base_s.html"
    elif (role == 'Customer'):
        navbar = "base_nobot.html"
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
    return render_template('paypal/customer_credit_form.html', form=CreditCard, shopping_list = shopping_list,navbar = navbar,cust_details=cust_details )


if __name__ == '__main__':
    app.run(debug=True)
