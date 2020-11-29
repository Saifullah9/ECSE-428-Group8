from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api import main
from uuid import UUID

"""
Step Definitions for ID012_Create_School_Supply_Purchase_Checklist
"""

    
# Given step for logging on is also found in ID015_steps.py

@given("user has a school supply list")
def step_impl(context):
    image_file = open("features/test_files/morris_supply.pdf", "rb")
    context.image_file = image_file
    context.file_content_type = 'application/pdf'
    context.file_name = "morris_supply.pdf"
    context.file_obj = {'file': (context.file_name, context.image_file, context.file_content_type)}
    context.headers = {"Authorization": "Bearer " + context.access_token}
    context.response_upload = context.test_client.post("/upload", files=context.file_obj, headers=context.headers)
    context.school_supply_id = context.response_upload.json()['school_supply_id']

@when("user requests a school supply purchase checklist")
def step_impl(context):
    context.response_download = context.test_client.get("/download", headers=context.headers)
    context.response_download_json = context.response_download.json()

@then("a new checklist is created with checkboxes next to each item")
def step_impl(context):
    for supply_list in context.response_download_json["supply_lists"]:
        for item in supply_list["list_of_supplies"]:
            assert len(item) == 2
        # print(item)
    metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    data_sess = MongoSessionRegular(collection="school_supplies")
    metadata_sess.delete_json({"email": context.login['username']})
    data_sess.remove_supply_list(UUID(context.school_supply_id))
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": "kaldamzxmczk12@hotmail.com"})
    

@given("user does not have a school supply list")
def step_impl(context):
    context.headers = {"Authorization": "Bearer " + context.access_token}


@then('"{error_message}" message is shown')
def step_impl(context, error_message):
    print(context.response_download_json["detail"])
    assert context.response_download_json["detail"] == error_message
    user_sess = MongoSessionRegular(collection='users')
    user_sess.delete_json({"email": "kaldamzxmczk12@hotmail.com"})