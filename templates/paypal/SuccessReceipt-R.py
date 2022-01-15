import pyodbc
def success_payment():
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    receipt_details ={}
    cursor = conn.cursor()
    cursor.execute('SELECT OrderID,POSDate,Totalprice from CustOrder')
    cursor_data = cursor.fetchall()
    for i in cursor_data:
        orderID = [i[0]]
        date = [i[1]]
        total_price = [i[2]]
        print(orderID,date,total_price)
        receipt_details.update({i[0]:i[0],i[0]:i[2]})
success_payment()
