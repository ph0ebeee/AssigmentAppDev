#using this pyhton file to store all the database functions that needs to be called in HTML file

#functions for customerSettings.html
def customerParticulars():
    try:
        conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                        'Server=(localdb)\MSSQLLocalDB;'
                        'Database=EcoDen;'
                        'Trusted_Connection=yes;')
    except:
        return "impossible to connect to the database"

    #code to execute SQL code for Customer's particulars
    cursor = conn.cursor()
    query = 'SELECT * from Customer WHERE EmailAddr ={}'.format()
    cursor.execute(query)

    #code to fetch result of the SQL code output for Customer's particulars
    cursor_data = cursor.fetchall()

    #use for loop to check whether they have the same ID such that the html will only print customer's particulars when the customerSettings ID is matched with the account ID
