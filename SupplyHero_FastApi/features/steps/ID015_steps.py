from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api import main
from uuid import UUID

"""
Step Definitions for ID015_Edit_a_School_Supply_List
"""

    
@given('user is logged on')
def step_impl(context):
    context.test_client = TestClient(main.app)
    context.register = {"email": "kaldamzxmczk12@hotmail.com", "password": "a!s@d#" }
    context.response_register = context.test_client.post("/register", json=context.register)
    context.login = {"username": "kaldamzxmczk12@hotmail.com", "password": "a!s@d#"}
    context.response_login = context.test_client.post("/login", data=context.login)
    context.access_token = context.response_login.json()["access_token"]
    

@given("user has a school supply list's ID")
def step_impl(context):
    image_file = open("features/test_files/morris_supply.pdf", "rb")
    context.image_file = image_file
    context.file_content_type = 'application/pdf'
    context.file_name = "morris_supply.pdf"
    context.file_obj = {'file': (context.file_name, context.image_file, context.file_content_type)}
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.response_upload = context.test_client.post("/upload", files=context.file_obj, headers = context.headers)
    context.school_supply_id = context.response_upload.json()['school_supply_id']


@when("user requests to edit a school supply list with its' ID")
def step_impl(context):
    test_supply_list = {"old_id": context.school_supply_id, "list_of_supplies": ["fake_item1", "fake_item2"]}
    context.response_edit = context.test_client.put("/upload", json=test_supply_list, headers=context.headers)
    context.response_edit_json = context.response_edit.json()

@then("a new edited school supply list is updated in the user's account")
def step_impl(context):
    assert context.response_edit_json["Message"] == "Success"
    metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    data_sess = MongoSessionRegular(collection="school_supplies")
    metadata_sess.delete_json({"email": context.login['username']})
    data_sess.remove_supply_list(UUID(context.response_edit_json['school_supply_id']))

@when("the content of the school supply list is the same")
def step_impl(context):
    test_supply_list = {"old_id": context.response_edit_json['school_supply_id'], "list_of_supplies": ["fake_item1", "fake_item2"]}
    context.response_edit_error = context.test_client.put("/upload", json=test_supply_list, headers=context.headers)
    context.response_edit_error_json = context.response_edit_error.json()

@then('"{error_message}" message is displayed')
def step_impl(context, error_message):
    assert context.response_edit_error_json["detail"] == error_message
    metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    data_sess = MongoSessionRegular(collection="school_supplies")
    metadata_sess.delete_json({"email": context.login['username']})
    data_sess.remove_supply_list(UUID(context.response_edit_json['school_supply_id']))
