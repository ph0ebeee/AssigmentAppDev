
from flask import Flask, render_template, jsonify, request, url_for, redirect
import pyodbc
import shelve
import paypalrestsdk
from werkzeug.utils import redirect
from forms import forms
from templates.paypal.receipt import Receipt

# from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm
from forms.forms import signupForm

app = Flask(__name__)


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
        # receipt = Receipt.Receipt(transaction.id.trans_id,transaction.update_time.trans_time,transaction.amount.value.trans_value)
        # receipt_details[receipt.get_trans_id()] = receipt
        # db['Receipt'] = receipt_details
        # db.close
    return render_template('success_payment.html')

# shopping cart by Phoebe
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

@app.route('/ProductDelete', methods = ['POST'])
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





if __name__ == '__main__':
    app.run()
