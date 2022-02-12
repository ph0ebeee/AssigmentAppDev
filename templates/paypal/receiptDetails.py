import pyodbc
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

def send_receipt_details(OrderID,CustomerID,TotalPrice,POSDate):
    cursor = conn.cursor()
    query = "INSERT INTO CustOrder (OrderID,CustomerID,TotalPrice,POSDate) VALUES('{}','{}','{}',{})".format(OrderID,CustomerID,TotalPrice,POSDate)
    cursor.execute(query)
    conn.commit()
