# dont delete this file, its needed for trial and error when i am doing my loginValidation - Viona
import pyodbc

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

# code to execute SQL code for all products
cursor = conn.cursor()
cursor.execute('SELECT ProductName, ProductPrice from Product')

# code to fetch result of the SQL code output for all products
cursor_data = cursor.fetchall()

# organizing it into rows but idk if its even needed ?
for i in cursor_data:
    customerEmail_Password = [i[0]]
    print('name: ',customerEmail_Password)
    print('price: ', [i[1]])

# ask viona if need to spilt into the 3 categories
# ask viona about ratings in the database !

list 