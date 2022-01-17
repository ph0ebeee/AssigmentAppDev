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