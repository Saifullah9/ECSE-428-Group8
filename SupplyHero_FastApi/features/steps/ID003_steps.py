from behave import *
import jwt
import fastapi_users
from db.mongo_regular import MongoSessionRegular
from fastapi.testclient import TestClient
from api import main
from api.config import SECRET
from uuid import UUID

"""
Step Definitions for ID003_Log_In 
"""


@given('user has user has created an account with {email} and {password}')
def step_impl(context, email, password):
    context.mongo_sesh = MongoSessionRegular(collection='users')
    context.register = {"email": email, "password": password}
    context.test_client = TestClient(main.app)
    context.response = context.test_client.post("/register", json=context.register)
    print(context.response.json())
    context.user = email
    context.password = password


@when('user has requested to login with their correct {email} and {password}')
def step_impl(context, email, password):
    context.login = {"username": email, "password": password}
    context.response = context.test_client.post("/login", data=context.login)
    print(context.response.json())
    context.access_token = context.response.json()["access_token"]


@then('the {email} and {password} information is correct')
def step_impl(context, email, password):
    context.data = jwt.decode(context.access_token, SECRET, algorithms=['HS256'], audience="fastapi-users:auth")
    uuid_object = UUID(context.data["user_id"])
    user = context.mongo_sesh.find_json({"id": uuid_object})
    found_user = user["email"]
    found_pass = fastapi_users.password.get_password_hash(context.password)
    print(user)
    print(found_pass)
    assert found_user == email
    assert found_pass == password


@then('the user has logged in successfully')
def step_impl(context):
    context.status_code = context.response.status_code
    #TODO: need cleanup to remove entries from db
    context.mongo.sesh.delete_json({"user_id": context.data["user_id"]})
    assert context.status_code == 200
