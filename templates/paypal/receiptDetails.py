# Updating SQL by Wong Jun Yu Phoebe 210527H


import pyodbc
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

def send_receipt_details(CustomerID,TotalPrice,POSDate,OrderID):
    cursor = conn.cursor()
    IdentityINSERT_ON_sql = "SET IDENTITY_INSERT CustOrder ON"
    IdentityINSERT_OFF_sql = "SET IDENTITY_INSERT CustOrder OFF"

    queries = "SET IDENTITY_INSERT dbo.CustOrder ON"
    cursor.execute(queries)
    query = "INSERT INTO CustOrder (CustomerID,TotalPrice,POSDate,OrderID) VALUES ('{}','{}','{}','{}')".format(CustomerID,TotalPrice,POSDate,OrderID)
    print(query)
    cursor.execute(IdentityINSERT_ON_sql)
    cursor.execute(query)
    cursor.execute(IdentityINSERT_OFF_sql)
    # cursor.execute(query)
    conn.commit()

