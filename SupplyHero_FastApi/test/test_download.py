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


def test_download_one_list():

    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Upload file
    image_file = open("features/test_files/morris_supply.png", "rb")
    file_obj = {"file": ("morris_supply.png", image_file, "image/png")}
    upload_response = test_client.post("/upload", files=file_obj, headers=headers)
    upload_response_json = upload_response.json()

    # Add supply list UUID in class variable to get it deleted
    pytest.supply_ids.append(upload_response_json["school_supply_id"])

    # Download list
    download_response = test_client.get("/download", headers=headers)
    download_response_json = download_response.json()
    assert download_response.status_code == 200
    assert download_response_json["Message"] == "Success"
    assert len(download_response_json["supply_lists"]) == 1
    assert download_response_json["supply_lists"][0]["id"] == upload_response_json["school_supply_id"]
    

def test_download_multiple_lists():
    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Upload files
    image_file_1 = open("features/test_files/morris_supply.png", "rb")
    file_obj_1 = {"file": ("morris_supply.png", image_file_1, "image/png")}
    upload_response_1 = test_client.post("/upload", files=file_obj_1, headers=headers)
    upload_response_json_1 = upload_response_1.json()

    image_file_2 = open("features/test_files/grade2_supply_list.png", "rb")
    file_obj_2 = {"file": ("grade2_supply_list.png", image_file_2, "image/png")}
    upload_response_2 = test_client.post("/upload", files=file_obj_2, headers=headers)
    upload_response_json_2 = upload_response_2.json()

    # Download lists
    download_response = test_client.get("/download", headers=headers)
    download_response_json = download_response.json()

    # Add supply list UUIDs in class variable to get them deleted
    pytest.supply_ids.append(upload_response_json_1["school_supply_id"])
    pytest.supply_ids.append(upload_response_json_2["school_supply_id"])

    # Assertions
    assert download_response.status_code == 200
    assert download_response_json["Message"] == "Success"
    assert len(download_response_json["supply_lists"]) == 2
    assert download_response_json["supply_lists"][0]["id"] == upload_response_json_1["school_supply_id"]
    assert download_response_json["supply_lists"][1]["id"] == upload_response_json_2["school_supply_id"]


def test_download_no_list():
    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Download list
    download_response = test_client.get("/download", headers=headers)
    download_response_json = download_response.json()
    assert download_response.status_code == 400
    assert download_response_json["detail"] == "No file has been uploaded."
