class Feedback:
    count_id = 0

    def __init__(self, cust_name, email,feedback):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__cust_name = cust_name
        self.__email = email
        self.__feedback = feedback

    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_cust_name(self, cust_name):
        self.__cust_name = cust_name

    def set_email(self, email):
        self.__email = email

    def set_feedback(self, feedback):
        self.__feedback = feedback

    def get_feedback_id(self):
        return self.__feedback_id

    def get_cust_name(self):
        return self.__cust_name

    def get_email(self):
        return self.__email

    def get_feedback(self):
        return self.__feedback
