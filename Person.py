# class name
class Person:
    # class attribute, can be accessed by using class
    count_id = 0

    # initializer of class, must have in order to create the object
    # __init__ is also called when the object is created
    # i.e. p = Person('bobby', 'S1234567D')
    # self refers to the instance of the class
    # name and nric are parameters passed into the initializer
    def __init__(self, name, nric):
        # incrementing class attribute, count_id, by 1
        Person.count_id += 1

        ''' data (instance) attributes are accessible only by creating objects '''
        # private data (instance) attributes are defined using __
        # must be accessed using getter or setter methods
        self.__person_id = Person.count_id
        self.__nric = nric
        # public data (instance) attributes do not have __
        # can be called directly through the object
        self.name = name
        # there is a need to create a private attribute first even if no parameter passed in for it
        # this is to ensure later in the application you can call the getter setter methods for it
        self.__birthdate = None

    # getter method to retrieve nric, no parameters passed in
    # used to access private data (instance) attribute
    def get_nric(self):
        # returns the private attribute nric
        return self.__nric

    # setter method to change nric, 1 parameter (nric) is passed in
    # used to change private data (instance) attribute
    def set_nric(self, nric):
        # sets the value to the private attribute nric
        self.__nric = nric

    def get_birthdate(self):
        return self.__birthdate

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    # __str__ function is called when printing the object
    # i.e. print(p)
    def __str__(self):
        # returns the string
        return f'{self.name}\'s NRIC is {self.__nric} and birthdate is {self.get_birthdate()}'


''' test program in the same file '''
'''
# creating person object, calling the Person class and passing in the parameters
p = Person('bobby', 'S1234567B')
# printing the object that calls the __str__ function
print(p)
# changing name by accessing the public data attribute, name, directly
p.name = 'mary'
# changing nric by using setter method
# cannot change directly by calling p.__nric as it is private and inaccessible
p.set_nric('S5555555A')
# printing the object that calls the __str__ function
print(p)
'''
