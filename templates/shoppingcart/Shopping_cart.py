class Product:
    count_id = 0
    def __init__(self, product_id,product_name, product_price, total_price):
        Product.count_id += 1
        self.__count = Product.count_id
        self.__product_id = product_id
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_total_price = total_price

    def set_product_name(self,product_name):
        self.__product_name = product_name

    def set_product_price(self,product_price):
        self.__product_price = product_price

    def set_product_id(self,product_id):
        self.__product_id = product_id

    def set_count(self,count_id):
        self.__count = count_id

    def set_price(self,total_price):
        self.__product_total_price = total_price
         
    def get_count(self):
        return self.__count

    def get_price(self):
        return self.__product_total_price

    def get_product_id(self):
        return self.__product_id

    def get_product_name(self):
        return self.__product_name

    def get_product_price(self):
        return self.__product_price

