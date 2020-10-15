from model.student import Student

class User:

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.username = ""
        self.password = ""
        self.students = []

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_first_name(self):
        return self.first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_last_name(self):
        return self.last_name

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def add_student(self, student: Student):
        self.students.append(student)

    def get_students(self):
        return self.students 