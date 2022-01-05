<<<<<<< HEAD

from flask import Flask, render_template, jsonify, request, url_for, redirect

=======
from flask import Flask, render_template, jsonify, request, url_for, redirect
>>>>>>> 16f73f3575cdd6199165b14315382620a693d813
import paypalrestsdk
from werkzeug.utils import redirect
from forms import forms

#from templates.chatbot.chat import get_response
#from templates.Forms import CreateUserForm,CreateCustomerForm
from forms.forms import signupForm

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('staff.html')
    
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


#@app.route("/predict", methods=['POST'])
#def predict():
 #   text = request.get_json().get("message")
  #  response = get_response(text)
   # message = {"answer": response}
    #return jsonify(message)

@app.route("/ShoppingCart",methods = ["GET"])
def shopping_cart():
    return render_template('/shopping cart/shopping_cart.html')




paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AfRIwzrYKNDDjzhwa6wx4MAuoKf-7j0t76lAYyH-OEAC_XwtpxZmWX_VQ7M4INH10LUrIsESHWDFcUmm",
  "client_secret": "ELm9nAnFFJV46yrWD8GqCwqSViSw8wda7DGGBJnxmMe2v7mCVDHp88HwLRzhj_3ehT73-ZdUx2jfOr_O" })

@app.route('/checkout')
def index():
    return render_template('paypal.html')

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})


#@app.route('/contactUs', methods=['GET', 'POST'])
#def feedback():
 #   feedback = CreateUserForm(request.form)
  #  if request.method == 'POST' and feedback.validate():
   #     users_dict = {}
    #    db = shelve.open('user.db', 'c')

     #   try:
      #      users_dict = db['Users']
       # except:
        #    print("Error in retrieving Users from user.db.")

        #user = User.User(feedback.name.data, feedback.response.data)
        #users_dict[user.get_user_id()] = user
        #db['Users'] = users_dict





if __name__ == '__main__':
    app.run()
