# daphne's product section - retrieve from SQL to pycharm
import templates.products.Product as P
# import Product as P
import pyodbc

from forms.forms import createProduct


def discounted_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID, ProductPicture, ProductName, ProductPrice, StockCount, ProductDiscount, CreatedDate, ProductCategory FROM Product'
                   ' ORDER BY CreatedDate DESC')  # ask the SQL to give out the data

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []

    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product(i[0], i[1], i[2], i[3], float(i[3] * i[5]), i[4], i[6], i[7])
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
    cursor.execute('SELECT P.ProductID, P.ProductName, P.ProductPrice, P.ProductPicture, COUNT (C.ProductID) AS TOTAL FROM CustOrderDetails C'
                   ' JOIN Product P on P.ProductID = C.ProductID'
                   ' GROUP BY P.ProductID, P.ProductName, P.ProductPrice, P.ProductPicture'
                   ' ORDER BY TOTAL DESC')  # ask the SQL to give out the data

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []
    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product(i[0],i[3],i[1],i[2],'','','','')  # need to put some as empty string
        #print(i[5], i[7], product.get_product_Name())
        product_dict.append(product)  # ask mr bobby what is this for -> key to reference in somewhere else

    return product_dict


def newlyrestocked_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID, ProductName, ProductPrice, ProductPicture FROM Product'  # don't need the P. -> not using shortcut name for products
                   ' ORDER BY CreatedDate')        # ask the SQL to give out the data --> need change to newly restocked according to created date

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []
    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product(i[0],i[3],i[1],i[2],'','','','')  # need to put some as empty string
        #print(i[5], i[7], product.get_product_Name())
        product_dict.append(product)  # ask mr bobby what is this for -> key to reference in somewhere else

    return product_dict


def frozen_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID, ProductName, ProductPrice, ProductPicture FROM Product '
                   ' WHERE ProductCategory = \'Ice Cream\'')  # don't need the P. -> not using shortcut name for products
        # ask the SQL to give out the data --> need change to newly restocked according to created date

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []
    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product(i[0],i[3],i[1],i[2],'','','','')  # need to put some as empty string
        #print(i[5], i[7], product.get_product_Name())
        product_dict.append(product)  # ask mr bobby what is this for -> key to reference in somewhere else

    return product_dict


def grains_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID, ProductName, ProductPrice, ProductPicture FROM Product '
                   ' WHERE ProductCategory = \'Grains\'')  # don't need the P. -> not using shortcut name for products
        # ask the SQL to give out the data --> need change to newly restocked according to created date

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []
    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product(i[0],i[3],i[1],i[2],'','','','')  # need to put some as empty string
        #print(i[5], i[7], product.get_product_Name())
        product_dict.append(product)  # ask mr bobby what is this for -> key to reference in somewhere else

    return product_dict


def household_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    # code to execute SQL code for all products
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID, ProductName, ProductPrice, ProductPicture FROM Product '
                   ' WHERE ProductCategory = \'Household\'')  # don't need the P. -> not using shortcut name for products
        # ask the SQL to give out the data --> need change to newly restocked according to created date

    # code to fetch result of the SQL code output for all products
    cursor_data = cursor.fetchall()  # need to catch the data ourselves (inbuilt function)

    product_dict = []
    # organizing it into rows but idk if its even needed ?
    for i in cursor_data:
        product = P.Product(i[0],i[3],i[1],i[2],'','','','')  # need to put some as empty string
        #print(i[5], i[7], product.get_product_Name())
        product_dict.append(product)  # ask mr bobby what is this for -> key to reference in somewhere else

    return product_dict

# SELECT * FROM Product WHERE ProductCategory = 'Ice Cream'

def create_products(ProductCategory,ProductPicture,ProductName,ProductDesc,ProductPrice,StockCount,ProductDiscount,CreatedDate):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    form = createProduct(csrf_enabled=False)
    cursor = conn.cursor()
    query = "INSERT INTO Product (ProductCategory,ProductPicture,ProductName,ProductDesc,ProductPrice,StockCount,ProductDiscount,CreatedDate) " \
            "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(ProductCategory,ProductPicture,ProductName,ProductDesc,ProductPrice,StockCount,ProductDiscount,CreatedDate)
    cursor.execute(query)
    conn.commit()
    conn.close()

def ProductDetails(ProductID):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    query = "SELECT * from Product WHERE ProductID = '{}'".format(ProductID)
    cursor.execute(query)

    cursor_data = cursor.fetchall()
    ProductList = []
    for i in cursor_data:
        ProductList.append(i)

    return ProductList

def update_products(ProductCategory,ProductPicture,ProductName,ProductDesc,ProductPrice,StockCount,ProductDiscount,CreatedDate,ProductID):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    query = "UPDATE Product SET ProductCategory = '{}', ProductPicture = '{}', ProductName = '{}', ProductDesc = '{}', ProductPrice = '{}', " \
            "StockCount = '{}', ProductDiscount = '{}', CreatedDate = '{}' " \
            "WHERE ProductID = '{}'".format(ProductCategory,ProductPicture,ProductName,ProductDesc,ProductPrice,StockCount,ProductDiscount,CreatedDate,ProductID)
    cursor.execute(query)
    conn.commit()
    conn.close()

def delete_products(ProductID):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    query = "DELETE FROM Product WHERE ProductID = '{}'".format(ProductID)
    cursor.execute(query)
    conn.commit()
    conn.close()


def all_products():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')

    ProductList = []

    cursor = conn.cursor()
    query = "SELECT * from Product"
    cursor.execute(query)

    cursor_data = cursor.fetchall()

    for i in cursor_data:
        ProductList.append(i)

    return ProductList

# def delete_products(ProductID):
#    cursor = conn.cursor()
#    query = "DELETE FROM Product WHERE ProductID = '{}'".format(ProductID)
#    cursor.execute(query)
#    conn.commit()
