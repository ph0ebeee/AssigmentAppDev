#using this pyhton file to store all the database functions that needs to be called in HTML file
import pyodbc
from templates.customer.Customers import Customers

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

def CustomerPurchase(customerID):
    #declaration of variables
    purchase_hist = []

    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "SELECT * from CustOrder WHERE CustomerID = '{}'".format(customerID)
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        purchase_hist.append(i)

    return purchase_hist

def CustDetails(customerID):
    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "SELECT * from Customer WHERE CustomerID = '{}'".format(customerID)
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()
    custDetails = []
    for i in cursor_data:
        custDetails.append(i)

    return custDetails

def CustomerVoucher(customerID):
    #declaration of variables
    vouchers_list = []

    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "SELECT v.VoucherID,v.VoucherDescription, v.ValueCategory, v.VoucherValue, v.ExpiryDate FROM Voucher v INNER JOIN CustomerVoucher cv ON cv.VoucherID = v.VoucherID INNER JOIN Customer c ON cv.CustomerID = c.CustomerID WHERE cv.CustomerID = '{}'".format(customerID)
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        vouchers_list.append(i)

    return vouchers_list

def viewFAQ():
    #declaration of variables
    faq_List = []

    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "SELECT * FROM FAQ"
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        faq_List.append(i)

    return faq_List

def checkOOS_items():
    #declaration of variables
    oos_List = []

    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "select * from Product WHERE StockCount <= 20 ORDER BY StockCount Asc"
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        oos_List.append(i)

    return oos_List

def top_product():
    #declaration of variables
    top_products_list = []

    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "select p.ProductID, p.ProductName,p.ProductCategory, p.ProductDesc, p.ProductPrice, p.StockCount,COUNT(cod.ProductID) FROM CustOrderDetails cod INNER JOIN Product p ON cod.ProductID = p.ProductID GROUP BY p.ProductName,p.ProductCategory, p.ProductDesc, p.ProductPrice, p.StockCount, p.ProductID ORDER BY COUNT(cod.ProductID) DESC"
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        top_products_list.append(i)

    return top_products_list

def top_customer():
    #declaration of variables
    top_custs_list = []

    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "select c.CustomerID, c.CustomerName, c.EmailAddr, c.MembershipPoints, c.ContactNum, COUNT(co.CustomerID), ROUND(SUM(p.ProductPrice),2) FROM CustOrder co INNER JOIN Customer c ON co.CustomerID = c.CustomerID INNER JOIN CustOrderDetails cod ON co.OrderID = cod.OrderID INNER JOIN Product p ON cod.ProductID = p.ProductID GROUP BY c.CustomerID, c.CustomerName, c.EmailAddr, c.MembershipPoints, c.ContactNum ORDER BY SUM(ProductPrice) DESC"
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        top_custs_list.append(i)

    return top_custs_list