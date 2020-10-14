from behave import *
from db.mongo import MongoSession
from fastapi.testclient import TestClient
from fastapi import UploadFile
from api import main

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
    context.file_obj = {'file': (context.file_name, context.image_file, context.file_content_type)}
    context.response = context.test_client.post("/upload", files=context.file_obj)
    assert context.response.status_code == 200 

@then('user should receive a school supply list')
def step_impl(context):
    response_json = context.response.json()
    assert type(response_json['list']) is list 

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
    assert response_json['error'] == error_str