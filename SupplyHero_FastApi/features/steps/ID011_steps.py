from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
import jwt
from uuid import UUID
from api import main
# import random
import json

"""
Step Definitions for ID005_Register_Account 
"""


@given('user is logged on')
def step_impl(context):
    # rando = random.randint(1, 50000000)
    context.mongo_sesh = MongoSessionRegular(collection='users')
    context.email = "usertest690@example.com"

    context.password = "string"
    if context.mongo_sesh.find_json({"email": context.email}) is not None:
        context.mongo_sesh.delete_json({"email": context.email})
    context.client = TestClient(main.app)
    # add user in case not existing
    context.reg_response = context.client.post("/register", json={
        "email": context.email,
        "password": context.password
    })

    context.login_response = context.client.post("/login", data={"username": context.email, "password": context.password})


    context.user = context.mongo_sesh.find_json({"email": context.email})
    # assert user["is_active"]

    assert context.user is not None


@when('user requests to log out')
def step_impl(context):
    if context.user is not None:
        jwt_token = json.loads(context.login_response.content)
        jwt_token = jwt_token["access_token"]
    else:
        jwt_token = "abcdeft"
    headers = {"Authorization": "Bearer " + jwt_token}
    context.logout_response = context.client.post("/logout", headers=headers)


@then('user is logged out')
def step_impl(context):

    user = context.mongo_sesh.find_json({"email": context.email})
    print(user)
    print(user["is_active"])
    # print(user)
    # assert context.response.json()["email"] == context.register["email"]

    assert user["is_active"] == "false"
    # assert user is None


#Error flow
@given('user is not logged on')
def step_impl(context):
    context.mongo_sesh = MongoSessionRegular(collection='users')
    # rando = random.randint(1, 50000000)
    context.email = "usertest790@example.com"
    context.password = "string"
    if context.mongo_sesh.find_json({"email": context.email}) is not None:
        context.mongo_sesh.delete_json({"email": context.email})
    context.client = TestClient(main.app)
    # add user in case not existing
    context.reg_response = context.client.post("/register", json={
        "email": context.email,
        "password": context.password
    })


    context.user = None
    context.login_response = None
    assert context.reg_response.status_code == 201
    # assert  == 200
    # assert user is not None

# @when('user requests to log out')
# def step_impl(context):
#     response_json = context.response.json()
#     assert response_json["detail"] == "REGISTER_USER_ALREADY_EXISTS"
#     context.mongo_sesh.delete_json({"email": "kaldamzxmczk12@hotmail.com"})

@then('user is prompted "You are not logged in!" message')
def step_impl(context):
    print(context.logout_response.content)

    assert json.loads(context.logout_response.content)["detail"] == "Unauthorized"
