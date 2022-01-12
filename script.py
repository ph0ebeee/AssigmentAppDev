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