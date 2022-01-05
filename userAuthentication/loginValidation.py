#import database from sql server
import pyodbc
from forms.forms import loginForm

#connect SQL to python
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

#function to validate whether email and password input by user == input in the database
def validate_login_particulars():
    #declaration of variables
    form = loginForm(csrf_enabled=False)
    user_email = form.email 
    user_password = form.password
    staffEmail_Password = {}
    customerEmail_Password = {}

    #code to execute SQL code for Staff email
    cursor = conn.cursor()
    cursor.execute('SELECT EmailAddr,Password from Staff')

    #code to fetch result of the SQL code output for Staff's email
    cursor_data = cursor.fetchall()

    #change the Staff data format in dictionary form
    for i in cursor_data:
        staffEmail_Password.update( {i[0]:i[1]} )

    #code to execute SQL code for Customer's email    
    cursor1 = conn.cursor()
    cursor1.execute('SELECT EmailAddr,Password from Customer')

    #code to fetch result of the SQL code output for Customer's email
    cursor1_data = cursor1.fetchall()

    #change the Customer data format in dictionary form
    for i in cursor1_data:
        customerEmail_Password.update( {i[0]:i[1]} )
    
    #validation
    for i in staffEmail_Password:
        if user_email == i and user_password == staffEmail_Password[i]:
           cursor2 = conn.cursor()
           cursor2.execute('SELECT * From ')
           return redirect(url_for('staffHome')) #fix this redirection !!!!!!!!!!!!
        else:
           #ask user to re-input their particulars !!!!!!!!!!!!!!!!
           print('wrong staff email or password')
        break
           
    for i in staffEmail_Password:
        if user_email == i and user_password == customerEmail_Password[i]:
           return redirect(url_for('customerHome'))
        else:
           #ask user to re-input their particulars [once solved the redirect issue, probably use js] !!!!!!!!!!!!!!!!!!!
           print('wrong customer email or password')  
        break

validate_login_particulars()

#what i need to do {done}
#1. create a loop that checks users email and password input thru the staff and cust dictionary in 2 seperate loops
#2. if its correct staff will go staff customer go customer
