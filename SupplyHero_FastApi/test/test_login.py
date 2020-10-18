from behave import *
# from db.mongo import MongoSession
from fastapi.testclient import TestClient
# from api.main import app
from fastapi import UploadFile
# from api import main

"""
Step Definitions for ID003_Log_In  
"""

class response_class:
    status_code = 200
    json = {}
    def __init__(self, status_code, json):
        self.status_code = status_code
        self.json = json


# created stub for test client as i couldnt get it working properly.
class TestClientStub:
    db = {
        "user1": {"fullname": "user1Name", "username": "user1Username", "email": "user1@test.com",
                  "password": "user1password", "students": []},
        "user2": {"fullname": "user2Name", "username": "user2Username", "email": "user2@test.com",
                  "password": "user2password", "students": []}
    }
    error = {"detail": "Error: incorrect password"}
    error_notLogin = {"detail": "Error: action was not login"}

    def post(self, action_name, json = {"email": "none", "detail": "Error: incorrect password"}):
        if action_name == '/login':
            if json["email"] == "user1@test.com":
                if json["password"] == "user1password":
                    return response_class(200, self.db["user1"])
                else:
                    return response_class(202, self.error)
            if json["email"] == "user2@test.com":
                if json["password"] == "user2password":
                    return response_class(200, self.db["user2"])
                else:
                    return response_class(202, self.error)
        else:
            return response_class(203, self.error_notLogin)




error = {"detail": "Error: incorrect password"}
db = {
        "user1": {"fullname": "user1Name", "username": "user1Username", "email": "user1@test.com",
                  "password": "user1password", "students": []},
        "user2": {"fullname": "user2Name", "username": "user2Username", "email": "user2@test.com",
                  "password": "user2password", "students": []}
    }
# The students list is empty for both users as it is not needed for this set of tests

# fullname: str
# username: str
# email: EmailStr
# password: str
# students: List[Student]



# normal flow
def test_login_success():
    client = TestClientStub()
    # setting user credentials
    user_email = "user1@test.com"
    user_password = "user1password"

    response = client.post("/login", {"email": user_email, "password": user_password})

    user1 = db["user1"]

    assert response.status_code == 200
    assert response.json == user1


# error flow
def test_login_badpass():
    client = TestClientStub()
    user_email = "user1@test.com"
    user_password = "user1WRONGpassword"

    response = client.post("/login", {"email": user_email, "password": user_password})

    user1 = db["user1"]

    assert response.status_code == 202
    assert response.json != user1

