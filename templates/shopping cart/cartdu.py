# shopping cart by Phoebe
# @app.route("/ShoppingCart",methods = ["GET"])
# def shopping_cart():
#     return render_template('shopping cart/shopping_cart.html')
#

# @app.route('/ShoppingCart', methods = ['POST'])
# def add_product():
#     cart_product = {}
#     db = shelve.open(cart_product)
#
#     try:
#         cart_product = db['Products']
#     except:
#         print("Error in retrieving Products from products.db")
#
#     conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                       'Server=(localdb)\MSSQLLocalDB;'
#                       'Database=EcoDen;'
#                       'Trusted_Connection=yes;')
#     cursor = conn.cursor()
#     cursor.execute('SELECT ProductName from Product')
#     cursor_data = cursor.fetchall()
#     for i in cursor_data:
#         cart_product.update( {i[0]:i[1]} )
#
# @app.route('/deleteProduct', methods = ['POST'])
# def delete_product():
#     pass

# @app.route('/add', methods=['POST'])
# def add_product_to_cart():
# 	try:
#             conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                               'Server=(localdb)\MSSQLLocalDB;'
#                               'Database=EcoDen;'
#                               'Trusted_Connection=yes;')
#             cart_product = {}
#             cursor = conn.cursor()
#             cursor.execute('SELECT ProductName from Product')
#             cursor_data = cursor.fetchone()
#             for i in cursor_data:
#                 cart_product.update({i[0]:i[1]}) #change the array to the suitable variable
#                 all_total_price = 0
#                 all_total_quantity = 0
#
#                 for key, value in session['cart_item'].items():
#                     if cursor_data['code'] == key:
#                         #session.modified = True
#                         #if session['cart_item'][key]['quantity'] is not None:
#                         #	session['cart_item'][key]['quantity'] = 0
#                         old_quantity = ['cart_item'][key]['quantity']
#                         total_quantity = old_quantity + _quantity
#                         ['cart_item'][key]['quantity'] = total_quantity
#                         ['cart_item'][key]['total_price'] = total_quantity * cursor_data['price']
# 				else:
# 					['cart_item'] = array_merge(session['cart_item'], itemArray)
#
# 				for key, value in session['cart_item'].items():
# 					individual_quantity = int(session['cart_item'][key]['quantity'])
# 					individual_price = float(session['cart_item'][key]['total_price'])
# 					all_total_quantity = all_total_quantity + individual_quantity
# 					all_total_price = all_total_price + individual_price
# 			else:
# 				session['cart_item'] = itemArray
# 				all_total_quantity = all_total_quantity + _quantity
# 				all_total_price = all_total_price + _quantity * cursor_data['price']
#
# 			session['all_total_quantity'] = all_total_quantity
# 			session['all_total_price'] = all_total_price
#
# 			return redirect(url_for('.products'))
# 		else:
# 			return 'Error while adding item to cart'
#     finally:
#         pass
#
# @app.route('/')
# def products():
# 	try:
#             conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                               'Server=(localdb)\MSSQLLocalDB;'
#                               'Database=EcoDen;'
#                               'Trusted_Connection=yes;')
#             cart_product = {}
#             cursor = conn.cursor()
#             cursor.execute('SELECT ProductName from Product')
#             cursor_data = cursor.fetchall()
#             for i in cursor_data:
#                 cart_product.update({i[0]:i[1]}) #change the array to the suitable variable
#             return render_template('products.html', products=cursor_data)
# 	finally:
# 		cursor.close()
# 		conn.close()
#
#
# @app.route('/delete')
# def delete_product():
# 	try:
# 		all_total_price = 0
# 		all_total_quantity = 0
#                 for key, value in ['cart_item'].items():
#                     individual_quantity = int(['cart_item'][key]['quantity'])
#                     individual_price = float(['cart_item'][key]['total_price'])
#                     all_total_quantity = all_total_quantity + individual_quantity
#                     all_total_price = all_total_price + individual_price
#
# 		# if all_total_quantity == 0:
# 		# 	session.clear()
# 		# else:
# 		# 	session['all_total_quantity'] = all_total_quantity             WORK ON THESE!!!
# 		# 	session['all_total_price'] = all_total_price
#
# 		# return redirect('/')
# 		return redirect(url_for('.products'))
#     finally:
#         pass
#
# def array_merge( first_array , second_array ):
# 	if isinstance( first_array , list ) and isinstance( second_array , list ):
# 		return first_array + second_array
# 	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
# 		return dict( list( first_array.items() ) + list( second_array.items() ) )
# 	elif isinstance( first_array , set ) and isinstance( second_array , set ):
# 		return first_array.union( second_array )
# 	return False
