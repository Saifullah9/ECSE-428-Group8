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


def test_upload_valid_img():
    image_file = open("features/test_files/morris_supply.png", "rb")
    file_obj = {"file": ("morris_supply.png", image_file, "image/png")}
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}
    response = test_client.post("/upload", files=file_obj, headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["Message"] == "Success"
    pytest.supply_ids.append(response_json["school_supply_id"])


def test_upload_invalid_img():
    image_file = open("features/test_files/test.txt", "rb")
    file_obj = {"file": ("test.txt", image_file, "test/plain")}
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}
    response = test_client.post("/upload", files=file_obj, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "File is not an image."


def test_upload_valid_pdf():
    image_file = open("features/test_files/morris_supply.pdf", "rb")
    file_obj = {"file": ("morris_supply.pdf", image_file, "application/pdf")}
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}
    response = test_client.post("/upload", files=file_obj, headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["Message"] == "Success"
    pytest.supply_ids.append(response_json["school_supply_id"])



def test_upload_not_authorized():
    image_file = open("features/test_files/morris_supply.png", "rb")
    file_obj = {"file": ("morris_supply.png", image_file, "image/png")}
    response = test_client.post("/upload", files=file_obj)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
