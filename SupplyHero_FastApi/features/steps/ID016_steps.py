from behave import *
from db.mongo import MongoSessionRegular
from fastapi.testclient import TestClient
from fastapi import UploadFile
import jwt
from uuid import UUID
from api import main
import uuid
# import random
import json




@given('user has an account with at least one supply list')
def step_impl(context):
    pass
    # context.client = TestClient(main.app)
    # context.mongo_sesh = MongoSessionRegular(collection='users')
    # context.metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    # context.data_sess = MongoSessionRegular(collection="school_supplies")
    # context.uuid_temp = uuid.uuid4()
    # context.metadata_sess.upsert_supply_list_metadata_email("myemail@gmail.com", context.uuid_temp)


@when('user requests to delete this school supply list')
def step_impl(context):
    context.delete_list_response = context.client.delete("/List?supply_list_id=" + str(context.uuid_temp) + "&email=myemail%40gmail.com")


@then('the school supply list no longer exists for this user')
def step_impl(context):
    assert json.loads(context.delete_list_response.content)["Message"] == "Success, id has been removed"


@given('user who already have an existing account with no supply lists')
def step_impl(context):
    pass
    # context.client = TestClient(main.app)
    # context.mongo_sesh = MongoSessionRegular(collection='users')
    # context.metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    # context.data_sess = MongoSessionRegular(collection="school_supplies")
    # context.uuid_temp = uuid.uuid4()
    # context.metadata_sess.upsert_supply_list_metadata_email("myemail@gmail.com", context.uuid_temp)


@then('user is shown "You have no school supply lists." message')
def step_impl(context):
    assert json.loads(context.delete_list_response.content)["Message"] == "No Changes Made"
