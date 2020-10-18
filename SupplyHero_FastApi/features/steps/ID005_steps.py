from behave import *
from db.mongo import MongoSession
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api import main
import jwt
from uuid import UUID
from fastapi.testclient import TestClient
from api import main
from api.config import SECRET

"""
Step Definitions for ID005_Register_Account 
"""

@given('user does not have an existing account with given {email}')
def step_impl(context, email):
    context.mongo_sesh = MongoSession(collection='users')
    context.data = jwt.decode(context.access_token, SECRET, algorithms=['HS256'], audience="fastapi-users:auth")
    uuid_object = UUID(context.data["user_id"])
    user = context.mongo_sesh.find_json({"id": uuid_object})
    found_user = user["email"]
    #TODO found_user should return to false



@when('user has requested to register with the {email} and {password}')
def step_impl(context, email, password):
    context.register = {"email": email, "password": password}
    context.response = context.test_client.post("/register", data=context.register)
    context.access_token = context.response.json()["access_token"]
@then('a new account is created with the given {email} and {password} ')
def step_impl(context, email, password):
    context.data = jwt.decode(context.access_token, SECRET, algorithms=['HS256'], audience="fastapi-users:auth")
    uuid_object = UUID(context.data["user_id"])
    user = context.mongo_sesh.find_json({"id": uuid_object})
    found_user = user["email"]
    assert found_user == email


@given('user has an existing account with given {email}')
def step_impl(context,email,password):
    context.mongo_sesh = MongoSession(collection='users')
    context.data = jwt.decode(context.access_token, SECRET, algorithms=['HS256'], audience="fastapi-users:auth")
    uuid_object = UUID(context.data["user_id"])
    user = context.mongo_sesh.find_json({"id": uuid_object})
    found_user = user["email"]
@then('user is informed that account exists')
def step_impl(context, error_str):
    response_json = context.response.json()
    assert response_json['An account with that email already exists.'] == error_str


