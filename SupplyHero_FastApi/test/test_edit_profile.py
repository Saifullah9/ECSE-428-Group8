from fastapi.testclient import TestClient
from uuid import UUID
from api.main import app
from db.mongo import MongoSessionRegular
import pytest

test_client = TestClient(app)

pytest.login_info = {"username": "parent@hotmail.com", "password": "a!s@d#"}

def test_edit_email():

    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Edit email
    new_email = "parentA@hotmail.com"
    edit_response = test_client.put("/editProfile", json={"email": new_email}, headers=headers)
    edit_response_json = edit_response.json()
    assert edit_response.status_code == 200
    assert edit_response_json["Message"] == "Success"
    assert edit_response_json["Email"] == new_email

    # Edit back to original email
    new_email = pytest.login_info["username"]
    edit_response = test_client.put("/editProfile", json={"email": new_email}, headers=headers)
    edit_response_json = edit_response.json()
    assert edit_response.status_code == 200
    assert edit_response_json["Message"] == "Success"
    assert edit_response_json["Email"] == new_email


def test_edit_existing_email():
    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Edit existing email
    new_email = pytest.login_info["username"]
    edit_response = test_client.put("/editProfile", json={"email": new_email}, headers=headers)
    edit_response_json = edit_response.json()
    assert edit_response.status_code == 400
    assert edit_response_json["detail"] == "Email is already used."


def test_edit_password():
    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Edit password
    new_password = "passWord123"
    edit_response = test_client.put("/editProfile", json={"password": new_password}, headers=headers)
    edit_response_json = edit_response.json()
    assert edit_response.status_code == 200
    assert edit_response_json["Message"] == "Success"
    assert edit_response_json["Email"] == pytest.login_info["username"]

    # Edit back to original password
    new_password = pytest.login_info["password"]
    edit_response = test_client.put("/editProfile", json={"password": new_password}, headers=headers)
    edit_response_json = edit_response.json()
    assert edit_response.status_code == 200
    assert edit_response_json["Message"] == "Success"
    assert edit_response_json["Email"] == pytest.login_info["username"]

def test_edit_empty():
    # Login
    login_response = test_client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

    # Edit without credentials
    edit_response = test_client.put("/editProfile", json={}, headers=headers)
    edit_response_json = edit_response.json()
    assert edit_response.status_code == 400
    assert edit_response_json["detail"] == "An email or password is needed."

