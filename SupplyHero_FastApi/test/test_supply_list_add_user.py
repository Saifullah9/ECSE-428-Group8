from fastapi.testclient import TestClient

from api.main import app
import pytest

client = TestClient(app)


def test_supply_list_add_user():
    # verify ids associated with the supply list

    pytest.login_info = {
        "username": "addUserTester@gmail.com", "password": "123456"}
    login_response = client.post("/login", data=pytest.login_info)
    headers = {"Authorization": "Bearer " +
               login_response.json()["access_token"]}

    # add a user as readonly to that supply list
    read_response = client.post("/addUser", json={
        "email": "targetuser@gmail.com",
        "privilege_type": "READ_ONLY",
        "supply_list_id": "bb7925b7-741c-4448-8b3a-160f39ae5204"
    })
    read_response_json = read_response.json()
    assert read_response_json["Message"] == "Success"

    # add a user as admin to that supply list
    admin_response = client.post("/addUser", json={
        "email": "targetuser@gmail.com",
        "privilege_type": "ADMIN",
        "supply_list_id": "bb7925b7-741c-4448-8b3a-160f39ae5204"
    })

    admin_response_json = admin_response.json()
    assert admin_response_json["Message"] == "Success"
