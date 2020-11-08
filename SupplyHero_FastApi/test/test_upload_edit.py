from fastapi.testclient import TestClient
from uuid import UUID
from api.main import app
from db.mongo import MongoSessionRegular
import pytest

test_client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    pytest.login_info = {"username": "parent@hotmail.com", "password": "a!s@d#"}
    pytest.supply_ids = []
    yield
    # Tear Down
    # Remove supply list data and metadata
    metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
    data_sess = MongoSessionRegular(collection="school_supplies")

    for id in pytest.supply_ids:
        metadata_sess.remove_supply_list_metadata(
            pytest.login_info["username"], UUID(id)
        )
        data_sess.remove_supply_list(
            UUID(id)
        )
    metadata_sess.delete_json({"email": pytest.login_info["username"]})

def test_edit_upload_list_valid():

    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Upload file
    image_file = open("features/test_files/morris_supply.pdf", "rb")
    file_obj = {"file": ("morris_supply.pdf", image_file, "application/pdf")}
    upload_response = test_client.post("/upload", files=file_obj, headers=headers)
    upload_response_json = upload_response.json()

    # Add supply list UUID in class variable to get it deleted
    pytest.supply_ids.append(upload_response_json["school_supply_id"])

    # Edit list
    test_supply_list = {"old_id": upload_response_json["school_supply_id"], "list_of_supplies": ["fake_item1", "fake_item2"]}
    edit_response = test_client.put("/upload", json=test_supply_list, headers=headers)
    edit_response_json = edit_response.json()
    pytest.supply_ids.append(edit_response_json["school_supply_id"])

    assert edit_response_json["Message"] == "Success"


def test_edit_upload_list_same_content():

    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Upload file
    image_file = open("features/test_files/morris_supply.pdf", "rb")
    file_obj = {"file": ("morris_supply.pdf", image_file, "application/pdf")}
    upload_response = test_client.post("/upload", files=file_obj, headers=headers)
    upload_response_json = upload_response.json()

    # Add supply list UUID in class variable to get it deleted
    pytest.supply_ids.append(upload_response_json["school_supply_id"])

    # Edit list
    test_supply_list = {"old_id": upload_response_json["school_supply_id"], "list_of_supplies": ["fake_item1", "fake_item2"]}
    edit_response = test_client.put("/upload", json=test_supply_list, headers=headers)
    edit_response_json = edit_response.json()
    pytest.supply_ids.append(edit_response_json["school_supply_id"])

    test_supply_list = {"old_id": edit_response_json["school_supply_id"], "list_of_supplies": ["fake_item1", "fake_item2"]}
    edit_response = test_client.put("/upload", json=test_supply_list, headers=headers)
    edit_response_json = edit_response.json()

    assert edit_response_json["detail"] == "The school supply list is the same"

def test_edit_upload_list_nonexistent_list():

    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}


    # Edit list
    # UUID is v4, should never be possibly generated from v5
    test_supply_list = {"old_id": 'dde18bae-75ba-4cbe-aa28-9858124a2dd1', "list_of_supplies": ["test1"]}
    edit_response = test_client.put("/upload", json=test_supply_list, headers=headers)
    edit_response_json = edit_response.json()

    assert edit_response_json["detail"] == "No School Supply list with ID: dde18bae-75ba-4cbe-aa28-9858124a2dd1"
