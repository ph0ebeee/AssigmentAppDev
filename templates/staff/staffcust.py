import pyodbc

def orders():
    try:
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')
    except:
        return "Impossible to connect to the database, check your code"

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CustOrder')
    data = cursor.fetchall()
    return data


