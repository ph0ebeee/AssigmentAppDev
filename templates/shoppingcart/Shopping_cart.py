import pyodbc
import shelve
import root as root
import datetime as datetime

class Product(root.Root):

    def __init__(self, product_id,product_name, product_price,quantity ):
        super().__init__(custID, datetime.datetime.now(), 'Phoebe', datetime.datetime.now())    #first is userid, datetime(module)
        self.__product_id = product_id
        self.__product_name = product_name
        self.__product_price = product_price

    def set_product_name(self,product_name):
        self.__product_name = product_name

    def set_product_price(self,product_price):
        self.__product_price = product_price

    def set_product_id(self,product_id):
        self.__product_id = product_id

    def get_product_id(self):
        return self.__product_id

    def get_product_name(self):
        return self.__product_name

    def get_product_price(self):
        return self.__product_price

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                  'Server=(localdb)\MSSQLLocalDB;'
                  'Database=EcoDen;'
                  'Trusted_Connection=yes;')
product_details ={}
cursor = conn.cursor()
cursor.execute('SELECT ProductID, ProductName, ProductPrice from Product')
cursor_data = cursor.fetchall()
for i in cursor_data:
    id = [i[0]]
    name = [i[1]]
    price = [i[2]]


    product_details = {}
    db = shelve.open('cart_product.db','c')

    try:
        product_details = db['Products']
    except:
        print("Error in retrieving Products from cart_product.db")

    p = Product(id,name, price)
    product = Product(p.set_product_id(id),p.set_product_name(name), p.set_product_price(price))

    product_details = product

    db['Products'] = product_details
    db.close()


# change what below!!! this one is to arrange?
#     user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.gender.data, create_user_form.membership.data, create_user_form.remarks.data)
#     users_dict[user.get_user_id()] = user




#     return redirect(url_for('retrieve_users'))
# return render_template('createUser.html', form=create_user_form)
