from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
import jwt
from uuid import UUID
from api import main

"""
Step Definitions for ID005_Register_Account 
"""


@given('user who does not have an existing account')
def step_impl(context):
    context.mongo_sesh = MongoSessionRegular(collection='users')
    user = context.mongo_sesh.find_json({"email": "kaldamzxmczk12@hotmail.com"})
    assert user is None


@when('user requests to register with the following information')
def step_impl(context):
    context.register = {"email": "kaldamzxmczk12@hotmail.com", "password": "a!s@d#" }
    context.test_client = TestClient(main.app)
    context.response = context.test_client.post("/register", json=context.register)


@then('a new account is created')
def step_impl(context):
    user = context.mongo_sesh.find_json({"email": "kaldamzxmczk12@hotmail.com"})
    print(user)
    assert context.response.json()["email"] == context.register["email"]
    assert user is not None

@given('user who already have an existing account')
def step_impl(context):
    context.mongo_sesh = MongoSessionRegular(collection='users')
    user = context.mongo_sesh.find_json({"email": "kaldamzxmczk12@hotmail.com"})

    assert user is not None

@then('user is informed that An account with that email already exists.')
def step_impl(context):
    response_json = context.response.json()
    assert response_json["detail"] == "REGISTER_USER_ALREADY_EXISTS"
    context.mongo_sesh.delete_json({"email": "kaldamzxmczk12@hotmail.com"})


