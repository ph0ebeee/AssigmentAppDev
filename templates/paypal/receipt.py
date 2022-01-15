class Receipt:
    count_id = 0

    def __init__(self, trans_id, trans_time, trans_value):
        Receipt.count_id += 1
        self.__trans_id = trans_id
        self.__trans_time = trans_time
        self.__trans_value = trans_value

    def get_trans_id(self):
        return self.__trans_id

    def get_trans_time(self):
        return self.__trans_time

    def get_trans_value(self):
        return self.__trans_value

    def set_trans_id(self, trans_id):
        self.__trans_id = trans_id

    def set_trans_time(self, trans_time):
        self.__trans_time = trans_time

    def set_trans_value(self, trans_value):
        self.__trans_value = trans_value
