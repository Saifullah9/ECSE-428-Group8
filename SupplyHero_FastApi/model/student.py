class Student:

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.school_name = ""
        self.school_supplies = []

    
    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_first_name(self):
        return self.first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_last_name(self):
        return self.last_name
    
    def set_school_supplies(self, supplies):
        self.school_supplies = supplies

    def get_school_supplies(self):
        return self.school_supplies

    def set_school_name(self, school_name):
        self.school_name = school_name

    def get_school_name(self):
        return self.school_name
    
