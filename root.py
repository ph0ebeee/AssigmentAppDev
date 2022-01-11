class Root:
    def __init__(self,created_by, created_date, modified_by, modified_date):
        self.__created_by = created_by
        self.__created_date = created_date
        self.__modified_by = modified_by
        self.__modified_date = modified_date

    def set_created_by(self,created_by):
        self.__created_by = created_by

    def set_created_date(self,created_date):
        self.__created_date = created_date

    def set_modified_by(self,modified_by):
        self.__modified_by = modified_by

    def set_modified_date(self,modified_date):
        self.__modified_date = modified_date

    def get_created_by(self):
        return self.__created_by

    def get_created_date(self):
        return self.__created_date

    def get_modified_by(self):
        return self.__modified_by

    def get_modified_date(self):
        return self.__modified_date
