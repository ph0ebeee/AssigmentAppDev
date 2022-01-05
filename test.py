# dont delete this file, its needed for trial and error when i am doing my loginValidation - Viona
import pyodbc

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT EmailAddr,Password from Staff')

cursor_data = cursor.fetchall()
staffEmail_Password = {}

for i in cursor_data:
    staffEmail_Password.update( {i[0]:i[1]} )


for i in staffEmail_Password:
    print(i)
    print(staffEmail_Password[i]+"\n")