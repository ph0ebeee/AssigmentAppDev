# Shopping Cart by Wong Jun Yu Phoebe 210527H

class cart_items:
    count_id = 0
    def __init__(self, product_id,product_name,product_image, product_price, total_price, product_quantity, total_quantity):
        cart_items.count_id += 1
        self.__count = cart_items.count_id
        self.__product_id = product_id
        self.__product_name = product_name
        self.__product_image = product_image
        self.__product_price = product_price
        self.__product_total_price = total_price
        self.__product_quantity = product_quantity
        self.__product_total_quantity = total_quantity

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_product_price(self, product_price):
        self.__product_price = product_price

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_count(self, count_id):
        self.__count = count_id

    def set_price(self, total_price):
        self.__product_total_price = total_price

    def set_product_image(self, product_image):
        self.__product_image = product_image

    def set_product_quantity(self, product_quantity):
        self.__product_quantity = product_quantity

    def get_product_quantity(self):
        return self.__product_quantity

    def set_product_total_quantity(self, total_quantity):
        self.__product_total_quantity = total_quantity

    def get_product_total_quantity(self):
        return self.__product_total_quantity

    def get_product_image(self):
        return self.__product_image
         
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

