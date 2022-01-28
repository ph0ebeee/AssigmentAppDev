import pyodbc
from forms.forms import createStaff
import bcrypt

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

def StaffDetails(StaffID):
    cursor = conn.cursor()
    query = "SELECT * from Staff WHERE StaffID = '{}'".format(StaffID)
    cursor.execute(query)

    cursor_data = cursor.fetchall()
    StaffList = []
    for i in cursor_data:
        StaffList.append(i)

    return StaffList

def CustDetails(customerID):

    cursor = conn.cursor()
    query = "SELECT * from Customer WHERE CustomerID = '{}'".format(customerID)
    cursor.execute(query)

    cursor_data = cursor.fetchall()
    custList = []
    for i in cursor_data:
        custList.append(i)

    return custList

def checkCust():

    custList = []

    cursor = conn.cursor()
    query = "SELECT * from Customer"
    cursor.execute(query)

    cursor_data = cursor.fetchall()

    for i in cursor_data:
        custList.append(i)

    return custList

def checkStaff():

    StaffList = []

    cursor = conn.cursor()
    query = "SELECT * from Staff"
    cursor.execute(query)

    cursor_data = cursor.fetchall()

    for i in cursor_data:
        StaffList.append(i)

    return StaffList

def updatestaff(StaffName,EmailAddr,Remarks,StaffID):

    cursor = conn.cursor()
    query = "UPDATE Staff SET StaffName = '{}', EmailAddr = '{}', Remarks = '{}' WHERE StaffID = '{}'".format(StaffName,EmailAddr,Remarks,StaffID)
    cursor.execute(query)
    conn.commit()

def updatecust(CustomerName,EmailAddr,MembershipPoints,ContactNum,ShippingAddr,CustomerID):

    cursor = conn.cursor()
    query = "UPDATE Customer SET CustomerName = '{}', EmailAddr = '{}', MembershipPoints = '{}', ContactNum = '{}', ShippingAddr = '{}' WHERE CustomerID = '{}'".format(CustomerName,EmailAddr,MembershipPoints,ContactNum,ShippingAddr,CustomerID)
    cursor.execute(query)
    conn.commit()

def updatestaffsettings(StaffName,EmailAddr,StaffID):

    cursor = conn.cursor()
    query = "UPDATE Staff SET StaffName = '{}', EmailAddr = '{}' WHERE StaffID = '{}'".format(StaffName,EmailAddr,StaffID)
    cursor.execute(query)
    conn.commit()

def createstaff(StaffName,EmailAddr,Password,Remarks):
    form = createStaff(csrf_enabled=False)
    password = form.password.data.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    salt = salt.decode('UTF-8')
    hashed = hashed.decode('UTF-8')
    cursor = conn.cursor()
    query = "INSERT INTO Staff (StaffName,EmailAddr,Password,passwordSalt,Remarks) VALUES ('{}', '{}','{}','{}','{}')".format(StaffName,EmailAddr,hashed,salt,Remarks)
    cursor.execute(query)
    conn.commit()

def deletestaff(StaffID):

    cursor = conn.cursor()
    query = "DELETE FROM Staff WHERE StaffID = '{}'".format(StaffID)
    cursor.execute(query)
    conn.commit()

def deletecust(CustomerID):

    cursor = conn.cursor()
    query = "DELETE FROM Customer WHERE CustomerID = '{}'".format(CustomerID)
    cursor.execute(query)
    conn.commit()

def addpoints(CustomerID):
    cursor = conn.cursor()
    query = "UPDATE Customer SET MembershipPoints += 100 WHERE CustomerID = '{}'".format(CustomerID)
    cursor.execute(query)
    conn.commit()
