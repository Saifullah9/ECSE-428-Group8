from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api import main
from uuid import UUID

"""
Step Definitions for ID008_Display_School_Supply_List
"""

@given('user logged in to the website')
def step_impl(context):
    context.test_client = TestClient(main.app)
    context.register = {"email": "kaldamzxmczk12@hotmail.com", "password": "a!s@d#" }
    context.response_register = context.test_client.post("/register", json=context.register)
    context.login = {"username": "kaldamzxmczk12@hotmail.com", "password": "a!s@d#"}
    context.response_login = context.test_client.post("/login", data=context.login)
    context.access_token = context.response_login.json()["access_token"]

@given("user has already uploaded at least one supply list")
def step_impl(context):
    image_file = open("features/test_files/morris_supply.pdf", "rb")
    context.image_file = image_file
    context.file_content_type = 'application/pdf'
    context.file_name = "morris_supply.pdf"
    context.file_obj = {'file': (context.file_name, context.image_file, context.file_content_type)}
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.response_upload = context.test_client.post("/upload", files=context.file_obj, headers = context.headers)
    context.school_supply_id = context.response_upload.json()['school_supply_id']

@when("user requests all school supply lists")
def step_impl(context):
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.response_download = context.test_client.get("/download", headers=context.headers)
    context.response_download_json = context.response_download.json()

@then("all lists of school supplies are displayed")
def step_impl(context):
    assert context.response_download_json["Message"] == "Success"
    metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    data_sess = MongoSessionRegular(collection="school_supplies")
    metadata_sess.delete_json({"email": context.login['username']})
    data_sess.remove_supply_list(UUID(context.school_supply_id))
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": context.login['username']})

@when("user has not uploaded any list of school supplies")
def step_impl(context):
    # User does not upload any list.
    pass

@then('a "{error_message}" message is displayed')
def step_impl(context, error_message):
    assert context.response_download_json["detail"] == error_message
    metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    metadata_sess.delete_json({"email": context.login['username']})
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": context.login['username']})
