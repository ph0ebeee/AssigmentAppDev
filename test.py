# dont delete this file, its needed for trial and error when i am doing my loginValidation - Viona
import pyodbc
import bcrypt

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

# code to execute SQL code for all products

password= "cust1234"
password = password.encode("utf-8")
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
#hashed = str.replace(hashed,"'","")
hashed = hashed.decode('UTF-8')
salt = salt.decode('UTF-8')
#print(salt)
#print(hashed)
#$2b$12$N609Eo8zdDLFl7a8Nv9lqOH0TTEhOhIhQAKnRi8ylpc7ixu.1ewfC
customerEmail_Password = {}
cursor = conn.cursor()
cursor.execute('SELECT EmailAddr,Password,passwordSalt from Customer')

#code to fetch result of the SQL code output for Customer's email
cursor_data = cursor.fetchall()

#change the Customer data format in dictionary form
for i in cursor_data:
    customerEmail_Password.update( {i[0]:[i[1],i[2]]} )

print(customerEmail_Password['joemarther@gmail.comm'])
print(customerEmail_Password['joemarther@gmail.comm'][0])
print(customerEmail_Password['joemarther@gmail.comm'][1])