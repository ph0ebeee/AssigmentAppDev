import root
import pyodbc


class Product(root.Root):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=(localdb)\MSSQLLocalDB;'
                      'Database=EcoDen;'
                      'Trusted_Connection=yes;')

    def __init__(self, created_by, created_date, modified_by, modified_date, product_name, product_price):
        super().__init__(created_by, created_date, modified_by, modified_date)
        self.__product_name = product_name
        self.__product_price = product_price
    super().__init__('Phoebe','12/1/2022','Phoebe','12/1/22')
