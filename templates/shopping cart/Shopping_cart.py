import pyodbc
import shelve

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')
product_details ={}
cursor = conn.cursor()
cursor.execute('SELECT ProductName, ProductPrice from Product')
cursor_data = cursor.fetchall()
for i in cursor_data:
    product_details.update({i[0]:i[1]})

    cart_product = {}
    db = shelve.open('cart_product.db','c')

    try:
        cart_product = db['Products']
    except:
        print("Error in retrieving Products from cart_product.db")
# change what below!!! this one is to arrange?
#     user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.gender.data, create_user_form.membership.data, create_user_form.remarks.data)
#     users_dict[user.get_user_id()] = user
#     db['Users'] = users_dict
#
#
#     db.close()
#     return redirect(url_for('retrieve_users'))
# return render_template('createUser.html', form=create_user_form)
