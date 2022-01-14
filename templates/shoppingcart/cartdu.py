import pyodbc
from flask import flash, session, render_template, request, redirect, url_for

def add_product_to_cart():
	cursor = None
	try:
		_quantity = int(request.form['quantity'])
		_code = request.form['code']
		# validate the received values
		if _quantity and _code and request.method == 'POST':
			conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
							  'Server=(localdb)\MSSQLLocalDB;'
							  'Database=EcoDen;'
							  'Trusted_Connection=yes;')
			cursor = conn.cursor()
			cursor.execute('SELECT ProductID, ProductName, ProductPrice from Product')
			cursor_data = cursor.fetchone()

			itemArray = { cursor_data['ProductID'] : {'name' : cursor_data['ProductName'], 'code' : cursor_data['ProductID'], 'price' : cursor_data['ProductPrice'], 'quantity' : _quantity, 'total_price': _quantity * cursor_data['ProductPrice']}}
			
			all_total_price = 0
			all_total_quantity = 0
			
			session.modified = True
			if 'cart_item' in session:
				if cursor_data['code'] in session['cart_item']:
					for key, value in session['cart_item'].items():
						if cursor_data['code'] == key:
							#session.modified = True
							#if session['cart_item'][key]['quantity'] is not None:
							#	session['cart_item'][key]['quantity'] = 0
							old_quantity = session['cart_item'][key]['quantity']
							total_quantity = old_quantity + _quantity
							session['cart_item'][key]['quantity'] = total_quantity
							session['cart_item'][key]['total_price'] = total_quantity * cursor_data['ProductPrice']
				else:
					session['cart_item'] = array_merge(session['cart_item'], itemArray)

				for key, value in session['cart_item'].items():
					individual_quantity = int(session['cart_item'][key]['quantity'])
					individual_price = float(session['cart_item'][key]['total_price'])
					all_total_quantity = all_total_quantity + individual_quantity
					all_total_price = all_total_price + individual_price
			else:
				session['cart_item'] = itemArray
				all_total_quantity = all_total_quantity + _quantity
				all_total_price = all_total_price + _quantity * cursor_data['ProductPrice']
			
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
			
			return redirect(url_for('.shopping_cart'))
		else:			
			return 'Error while adding item to cart'
	except Exception as e:
		print(e)

def backproduct():
	try:
		conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
						  'Server=(localdb)\MSSQLLocalDB;'
						  'Database=EcoDen;'
						  'Trusted_Connection=yes;')
		cursor = conn.cursor()
		cursor.execute('SELECT ProductID, ProductName, ProductPrice from Product')
		cursor_data = cursor.fetchall()
		return render_template('shopping_cart.html', products=cursor_data)
	except Exception as e:
		print(e)


def empty_cart():
	try:
		session.clear()
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)


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
		
		#return redirect('/')
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		
