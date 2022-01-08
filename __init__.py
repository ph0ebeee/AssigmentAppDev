from dns import transaction
from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
import pyodbc
import shelve
import paypalrestsdk
from templates.paypal.receipt import Receipt
from werkzeug.utils import redirect
from forms import forms
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, login_manager, LoginManager

from staff.staff_forms import UpdateAccountForm
from users import Users
#import os
#import secrets

# from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm
from forms.forms import signupForm

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'secretkey'
login_manager.login_view = 'login'
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

    
@app.route('/Login', methods=['GET', 'POST'])
#route for login form to be seen on loginPage.html
def login():
    loginPage = forms.loginForm(csrf_enabled=False)
    if request.method == 'POST' and loginPage.validate():
        return redirect(url_for('###'))
        #use JS to change the layout of the navbar according to Cust or Staff account
    return render_template('usersLogin/loginPage.html', form=loginPage)


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

@app.route('/Payment/Success', methods = ['POST'])
def success_payment():
    receipt_details = {}
    db = shelve.open['receipt.db','c']
    try:
        receipt_details = db['Receipt']
    except:
        print("Error in opening Receipt from receipt.db")
        receipt = Receipt.Receipt(transaction.id.trans_id,transaction.update_time.trans_time,transaction.amount.value.trans_value)
        receipt_details[receipt.get_trans_id()] = receipt
        db['Receipt'] = receipt_details
        db.close
    return render_template('success_payment.html')


# shopping cart by Phoebe
@app.route("/ShoppingCart",methods = ["GET"])
def shopping_cart():
    return render_template('shopping cart/shopping_cart.html')


@app.route('/ShoppingCart', methods = ['POST'])
def add_product():
    cart_product = {}
    db = shelve.open(cart_product)

    try:
        cart_product = db['Products']
    except:
        print("Error in retrieving Products from products.db")

    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute('SELECT ProductName from Product')
    cursor_data = cursor.fetchall()
    for i in cursor_data:
        cart_product.update( {i[0]:i[1]} )

@app.route('/deleteProduct', methods = ['POST'])
def delete_product():
    pass

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

#random idea anna
#def save_picture(form_picture):
#    random_hex = secrets.token_hex(8)
#    _, f_ext = os.path.splitext(form_picture.filename)
#    picture_path = os.path.join(app.root_path, 'Assets/images', picture_fn)
#
#    output_size = (125,125)
#    i = Image.open(form_picture)
#    i.thumbnail(output_size)
 #   i.save(picture_path)

 #   return picture_fn

# staff settings anna
@app.route("/staffaccount", methods=['GET', 'POST'])
@login_required
def staffaccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #picture_file = save_picture(form.picture.data)
            #current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            #db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('staffaccount'))
    elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
    #image_file = url_for('Assets', filename='images/' + current_user.image_file)
    return render_template('staff_account.html')
                           #title='Account',
                           #image_file=image_file, form=form)

if __name__ == '__main__':
    app.run()
