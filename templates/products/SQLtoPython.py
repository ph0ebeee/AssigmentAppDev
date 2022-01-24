# daphne's product section - retrieve from SQL to pycharm
import templates.products.Product as P
# import Product as P
import pyodbc


def discounted_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Product'
                   ' ORDER BY CreatedDate DESC')  # ask the SQL to give out the data

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []

    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product(i[0], i[2], i[4], i[4] * i[6], i[5], i[7])
        # print(i[4], i[6], product.get_discounted_price())
        product_dict.append(product)  # ask mr bobby what is this for -> key to reference in somewhere else

    return product_dict


def topselling_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT P.ProductName, P.ProductPrice, COUNT (C.ProductID) AS TOTAL FROM CustOrderDetails C'
                   ' JOIN Product P on P.ProductID = C.ProductID'
                   ' GROUP BY P.ProductName, P.ProductPrice'
                   ' ORDER BY TOTAL DESC')  # ask the SQL to give out the data

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []
    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product('', i[0], i[1],'','','')  # need to put some as empty string
        #print(i[4], i[6], product.get_product_Name())
        product_dict.append(product)  # ask mr bobby what is this for -> key to reference in somewhere else

    return product_dict