from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api import main
from uuid import UUID

"""
Step Definitions for ID002_Upload_Image  
"""

    
@given('user is selecting an image')
def step_impl(context):
    image_file = open("features/test_files/morris_supply.png", "rb")
    context.image_file = image_file
    context.file_content_type = 'image/png'
    context.file_name = 'morris_supply.png'

@when('user requests to upload the file')
def step_impl(context):
    context.test_client = TestClient(main.app)
    context.login_info = {"username": "parent@hotmail.com", "password": "a!s@d#"}
    context.file_obj = {'file': (context.file_name, context.image_file, context.file_content_type)}
    context.login_response = context.test_client.post("/login", data=context.login_info)
    context.headers = {"Authorization": "Bearer " + context.login_response.json()['access_token']}
    context.response = context.test_client.post("/upload", files=context.file_obj, headers = context.headers)


@then('user should receive a school supply list')
def step_impl(context):
    response_json = context.response.json()
    assert response_json['Message'] == 'Success'
    metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    data_sess = MongoSessionRegular(collection="school_supplies")
    response_json = context.response.json()
    metadata_sess.delete_json({"email":context.login_info['username']})
    delete_result = data_sess.remove_supply_list(UUID(response_json['school_supply_id']))


@given('user selected a file that is a PDF')
def step_impl(context):
    image_file = open("features/test_files/morris_supply.pdf", "rb")
    context.image_file = image_file
    context.file_content_type = 'application/pdf'
    context.file_name = 'morris_supply.pdf'


@given('user selected a file that is not an image or pdf')
def step_impl(context):
    text_file = open("features/test_files/test.txt", "rb")
    context.image_file = text_file
    context.file_content_type = 'text/plain'
    context.file_name = 'test.txt'


@then('user is informed that "{error_str}"')
def step_impl(context, error_str):
    response_json = context.response.json()
    assert response_json['detail'] == error_str