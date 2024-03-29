import templates.products.Base as Base

class Product(Base.Base):
    count_product_Id = 0
    def __init__(self, product_Id, product_Image, product_Name, product_Price, discounted_Price, product_Stock, created_date, product_Category):
        super().__init__(created_date)
        Product.count_product_Id += 1
        self.__product_Id = product_Id
        self.__product_Image = product_Image
        self.__product_Name = product_Name
        self.__product_Price = product_Price
        self.__discounted_Price = discounted_Price
        self.__product_Stock = product_Stock
        self.__product_Category = product_Category

    def set_product_Id(self, product_Id):
        self.__product_Id = product_Id

    def set_product_Image(self, product_Image):
        self.__product_Image = product_Image

    def set_product_Name(self, product_Name):
        self.__product_Name = product_Name

    def set_product_Price(self, product_Price):
        self.__product_Price = product_Price

    def set_discounted_Price(self, discounted_Price):
        self.__discounted_Price = discounted_Price

    def set_product_Stock(self, product_Stock):
        self.__product_Stock = product_Stock

    def set_product_Category(self, product_Category):
        self.__product_Category = product_Category

    def get_product_Id(self):
        return self.__product_Id

    def get_product_Image(self):
        return self.__product_Image

    def get_product_Name(self):
        return self.__product_Name

    def get_product_Price(self):
        return self.__product_Price

    def get_discounted_Price(self):
        return self.__discounted_Price

    def get_product_Stock(self):
        return self.__product_Stock

    def get_product_Category(self):
        return self.__product_Category
