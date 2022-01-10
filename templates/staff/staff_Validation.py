#import database from sql server
import pyodbc
from flask import flash

from staff_forms import UpdateAccount

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

#function to validate whether email input by user has recorded in the database
def validate_Staff_email():
    StaffEmail = []
    form = UpdateAccount(csrf_enabled=False)
    staff_email = form.email
    cursor = conn.cursor()
    cursor.execute('SELECT EmailAddr from Staff')

    cursor_data = cursor.fetchall()

    for i in cursor_data:
        StaffEmail.append(i)

    for i in StaffEmail:
        print(i)

    for i in StaffEmail:
        if staff_email == i:
            flash('This email has already been registered!', 'repeated')
        else:
            new_staff_email = UpdateAccount.email
            break

validate_Staff_email()
