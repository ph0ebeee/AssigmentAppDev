import pyodbc

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

def StaffDetails(StaffID):
    cursor = conn.cursor()
    query = "SELECT * from Staff WHERE StaffID = '{}'".format(StaffID)
    cursor.execute(query)

    cursor_data = cursor.fetchall()
    StaffDetails = []
    for i in cursor_data:
        StaffDetails.append(i)

    return StaffDetails

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

def updatestaff(StaffName,EmailAddr,StaffID):

    cursor = conn.cursor()
    query = "UPDATE Staff SET StaffName = '{}', EmailAddr = '{}' WHERE StaffID = '{}'".format(StaffName,EmailAddr,StaffID)
    cursor.execute(query)
    conn.commit()

def updatecust(CustomerName,EmailAddr,MembershipPoints,ContactNum,ShippingAddr,CustomerID):

    cursor = conn.cursor()
    query = "UPDATE Customer SET CustomerName = '{}', EmailAddr = '{}', MembershipPoints = '{}', ContactNum = '{}', ShippingAddr = '{}' WHERE CustomerID = '{}'".format(CustomerName,EmailAddr,MembershipPoints,ContactNum,ShippingAddr,CustomerID)
    cursor.execute(query)
    conn.commit()

def updatestaffsettings(StaffName,EmailAddr,Password,StaffID):

    cursor = conn.cursor()
    query = "UPDATE Staff SET StaffName = '{}', EmailAddr = '{}', Password = '{}' WHERE StaffID = '{}'".format(StaffName,EmailAddr,Password,StaffID)
    cursor.execute(query)
    conn.commit()
