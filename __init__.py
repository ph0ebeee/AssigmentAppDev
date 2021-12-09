from flask import Flask, render_template
#from templates.Forms import CreateUserForm,CreateCustomerForm


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')



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
