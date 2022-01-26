# dont delete this file, its needed for trial and error when i am doing my loginValidation - Viona
import pyodbc
import bcrypt

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

# code to execute SQL code for all products

password= input("heh:")
password = password.encode("utf-8")
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)

