from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api import main
from uuid import UUID

"""
Step Definitions for ID013_Edit_Profile
"""

@given("user is logged on with an active account")
def step_impl(context):
    context.test_client = TestClient(main.app)
    context.register = {"email": "kaldamzxmczk12@hotmail.com", "password": "a!s@d#" }
    context.response_register = context.test_client.post("/register", json=context.register)
    context.login = {"username": "kaldamzxmczk12@hotmail.com", "password": "a!s@d#"}
    context.response_login = context.test_client.post("/login", data=context.login)
    context.access_token = context.response_login.json()["access_token"]

@when("user edits their email address")
def step_impl(context):
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.test_email = {"email": "test123@gmail.com"}
    context.response_edit = context.test_client.put("/editProfile", json=context.test_email, headers=context.headers)
    context.response_edit_json = context.response_edit.json()

@then("the email address is updated on the user's profile")
def step_impl(context):
    assert context.response_edit_json["Message"] == "Success"
    assert context.response_edit_json["Email"] == context.test_email["email"]
    # Delete user
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": context.test_email["email"]})

@when("user edits their password")
def step_impl(context):
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.test_password = {"password": "pass123"}
    context.response_edit = context.test_client.put("/editProfile", json=context.test_password, headers=context.headers)
    context.response_edit_json = context.response_edit.json()

@then("the password is updated on the user's profile")
def step_impl(context):
    assert context.response_edit_json["Message"] == "Success"
    assert context.response_edit_json["Email"] == context.login["username"]
    # Delete user
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": context.login["username"]})

@when("user attempts to edit their email address with an existing one")
def step_impl(context):
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.test_email = {"email": context.login["username"]}
    context.response_edit = context.test_client.put("/editProfile", json=context.test_email, headers=context.headers)
    context.response_edit_error_json = context.response_edit.json()

@then('a "{error_message}" message is returned')
def step_impl(context, error_message):
    assert context.response_edit_error_json["detail"] == error_message
    # Delete user
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": context.login["username"]})

@when("user attempts to edit user profile without providing new information")
def step_impl(context):
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.test_no_info = {}
    context.response_edit = context.test_client.put("/editProfile", json=context.test_no_info, headers=context.headers)
    context.response_edit_error_json = context.response_edit.json()

@when("user attempts to edit their email address with an invalid one")
def step_impl(context):
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.test_invalid_email = {"email": "invalid_email"}
    context.response_edit = context.test_client.put("/editProfile", json=context.test_invalid_email, headers=context.headers)
    context.response_edit_error_json = context.response_edit.json()

@then('a "{error_message}" message is sent')
def step_impl(context, error_message):
    assert context.response_edit_error_json["detail"][0]["msg"] == error_message
    # Delete user
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": context.login["username"]})