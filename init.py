from flask import Flask, render_template
import pyodbc

app = Flask(__name__)


@app.route('/SuccessReceipt', methods =['POST'])
def retrieve_database_receipt():

    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                          'Server=(localdb)\MSSQLLocalDB;'
                          'Database=EcoDen;'
                          'Trusted_Connection=yes;')
    receipt_details ={}
    cursor = conn.cursor()
    cursor.execute('SELECT OrderID,POSDate,Totalprice from CustOrder')
    cursor_data = cursor.fetchall()
    return cursor_data


def receipt_display():
    to_send = retrieve_database_receipt()
    return render_template("templates/paypal/success_payment.html", to_send=to_send)


if __name__ == '__main__':
    app.run()
