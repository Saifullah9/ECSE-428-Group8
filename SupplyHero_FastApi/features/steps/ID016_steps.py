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

class TestDeleteStub:
    id_list = []

    def __init__(self):
        pass

    def upsert_supply_list_metadata_email(self, email, uuid_in):
        self.id_list.append(uuid_in)
        return "Success"

    def delete(self, url, uuid_in):
        for id in self.id_list:
            if id == uuid_in:
                return 200
        return 404

@given('user has an account with at least one supply list')
def step_impl(context):
    context.client = TestDeleteStub()
    context.uuid_temp = uuid.uuid4()
    context.client.upsert_supply_list_metadata_email("myemail@gmail.com", str(context.uuid_temp))


@when('user requests to delete this school supply list')
def step_impl(context):
    context.delete_response = context.client.delete("/List?supply_list_id=" + str(context.uuid_temp) + "&email=myemail%40gmail.com", str(context.uuid_temp))



@then('the school supply list no longer exists for this user')
def step_impl(context):
    assert context.delete_response == 200


@given('user who already have an existing account with no supply lists')
def step_impl(context):
    context.client = TestDeleteStub()
    context.uuid_temp = uuid.uuid4()


@then('user is shown "You have no school supply lists." message')
def step_impl(context):
    assert context.delete_response == 404

