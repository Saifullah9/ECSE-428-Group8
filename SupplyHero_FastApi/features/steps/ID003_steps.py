from behave import *
import jwt
import fastapi_users
from db.mongo import MongoSessionRegular
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
    context.response_register = context.test_client.post("/register", json=context.register)
    print(context.response_register.json())
    context.user = email
    context.password = password


@when('user has requested to login with their {email} and {password}')
def step_impl(context, email, password):
    context.login = {"username": email, "password": password}
    context.response_login = context.test_client.post("/login", data=context.login)
    # print(context.response_login.json())
    context.access_token = context.response_login.json()["access_token"]


@then('the {email} and {password} information is correct')
def step_impl(context, email, password):
    context.data = jwt.decode(context.access_token, SECRET, algorithms=['HS256'], audience="fastapi-users:auth")
    uuid_object = UUID(context.data["user_id"])
    user = context.mongo_sesh.find_json({"id": uuid_object})
    found_user = user["email"]
    found_hashed_pass = user['hashed_password']
    verified, __ = fastapi_users.password.verify_and_update_password(password, found_hashed_pass)
    assert found_user == email
    assert verified


@then('the user has logged in successfully')
def step_impl(context):
    context.status_code = context.response_login.status_code
    context.mongo_sesh.delete_json({"user_id": context.data["user_id"]})
    assert context.status_code == 200


@when('user has requested to login with their incorrect {bad_email} or {bad_password}')
def step_impl(context, bad_email, bad_password):
    context.login = {"username": bad_email, "password": bad_password}
    context.response_login = context.test_client.post("/login", data=context.login)
    # print(context.response_login.json())


@then('the {bad_email} and {bad_password} information is incorrect')
def step_impl(context, bad_email, bad_password):
    context.detail = context.response_login.json()["detail"]
    assert context.detail == "LOGIN_BAD_CREDENTIALS"


@then('an "Invalid Email/Password." message is shown')
def step_impl(context):
    context.status_code = context.response_login.status_code
    # TODO: need cleanup to remove entries from db
    # context_data = context.response_login.id
    # print(context_data)
    # context.mongo_sesh.delete_json({"user_id": context.data["user_id"]})
    assert (context.status_code == 400)
