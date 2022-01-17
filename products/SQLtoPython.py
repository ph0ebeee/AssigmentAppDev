# daphne's product section - retrieve from SQL to pycharm
import pyodbc

def products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT ProductName, ProductPrice from Product')  # ask the SQL to give out the data

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product_Name = [i[0]]  # fetch the first value in the data
        product_Price = [i[1]] # fetch the second value in the data
        print(product_Name)
        print(product_Price)


    # ask viona about ratings in the database !
