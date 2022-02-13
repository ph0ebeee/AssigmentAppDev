#using this pyhton file to store all the database functions that needs to be called in HTML file
import pyodbc
import jwt
import bcrypt
from itsdangerous.url_safe import URLSafeSerializer, URLSafeTimedSerializer
from templates.customer.Customers import Customers
from flask import Flask ,url_for,render_template
from django.core.mail import send_mail
from can import Message
import threading 

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

def RetrieveMonthlyOverallSalesRevenue(year):
    #declaration of variables
    average_revenue = []
    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "select MONTH(cod.POSDate) as Month, SUM(cod.TotalPrice) as TotalRevenueOfMonth FROM CustOrder cod WHERE YEAR(cod.POSDate) = "+str(year)+" GROUP BY  MONTH(cod.POSDate),YEAR(cod.POSDate) ORDER BY MONTH(cod.POSDate) ASC"
    cursor.execute(query)
    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()
    conn.commit()
    #change the Customer data format in dictionary form
    for i in cursor_data:
        average_revenue.append(i)

    return average_revenue

def RetrieveTopSellingProductCategory(month,year):
    #declaration of variables
    top_cat = []
    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "select p.ProductCategory, COUNT(p.ProductCategory) as 'Top Selling Categories' FROM CustOrderDetails cod INNER JOIN Product p ON cod.ProductID = p.ProductID WHERE Year(cod.POSDate) = "+str(year)+" AND Month(cod.POSDate) = "+str(month)+" GROUP BY p.ProductCategory"
    cursor.execute(query)
    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()
    conn.commit()
    #change the Customer data format in dictionary form
    for i in cursor_data:
        top_cat.append(i)

    return top_cat

def updatePassword(email, password):
    #declaration of variables
    purchase_hist = []

    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()

    query = "UPDATE Customer SET Password = '"+password+"' WHERE EmailAddr = '"+email+"'"
    cursor.execute(query)
    conn.commit()

    return ""+password+" "+email+""

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

def CustPwSalt(email):
    #code to execute SQL code for Customer's email & password
    cursor = conn.cursor()
    query = "SELECT PasswordSalt from Customer WHERE EmailAddr = '{}'".format(email)
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()
    custDetails = []
    for i in cursor_data:
        custDetails.append(i)

    return custDetails[0][0]

def send_password_reset_link(user_email, salt, app):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    password_reset_url = url_for(
        'reset_token',
        token = password_reset_serializer.dumps(user_email, salt=salt))
    print("2")
    html = render_template(
        'forgetPassword/password_reset.html',
        password_reset_url=password_reset_url)
    print("3")
    send_mail('Password Reset Requested',html,[app.config['MAIL_USERNAME']], [user_email])

def send_email_thread(msg, app,recipients):
    with app.app_context():
        print(recipients)
        send_mail(msg, (app.config['MAIL_USERNAME']),[recipients])

def send_email(subject, recipients, html_body, app):
    msg = Message(subject, recipients)
    msg.html = html_body
    thr = threading.Thread(target=send_email_thread(msg, app,recipients), args=[msg])
    thr.start()

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

def validated_Cust_Exists(email):
    #declaration of variables
    customerDetails = []
    #code to execute SQL code for Customer's email    
    cursor = conn.cursor()
    query = "SELECT * from Customer WHERE EmailAddr='{}'".format(email)
    cursor.execute(query) #error pyodbc.ProgrammingError: ('42000', "[42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]Incorrect syntax near '$2'. (102) (SQLExecDirectW)"

    #code to fetch result of the SQL code output for Customer's email
    cursor_data = cursor.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor_data:
        customerDetails.append(i)   

    if len(customerDetails) != 0:
        return True
    elif len(customerDetails) == 0:
        return False

RetrieveMonthlyOverallSalesRevenue(2021)