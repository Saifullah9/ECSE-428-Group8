from fastapi.testclient import TestClient
from db.mongo import MongoSessionRegular

import random
import json
from api.main import app

client = TestClient(app)
mongo_sesh = MongoSessionRegular(collection='users')
# test registering a new user, loggin them in, and then loggiing out the account PERMANENTLY. also
# Confirms account can no longer log in and db contains is_active=false
def test_logout_user():
    # rando = random.randint(1, 50000000)
    email = "usertest890@example.com"
    password = "string"
    if mongo_sesh.find_json({"email": email}) is not None:
        mongo_sesh.delete_json({"email": email})
    # add user in case not existing
    response = client.post("/register", json={
        "email": email,
        "password": password
    })

    # validate user email input
    assert response.json() != {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }
    # verify if existing user
    assert response.json() != {
        "detail": "REGISTER_USER_ALREADY_EXISTS"
    }

    assert response.json()["is_active"] == True
    login_response = client.post("/login", data={"username": email, "password": password})
    jwt_token = json.loads(login_response.content)
    jwt_token = jwt_token["access_token"]
    headers = {"Authorization": "Bearer " + jwt_token}

    logout_response = client.post("/logout", headers=headers)
    assert logout_response.json() == {"user_email": email, "logout_success": "true"}
    login_response_final = client.post("/login", data={"username": email, "password": password})
    assert json.loads(login_response_final.content)["detail"] == "LOGIN_BAD_CREDENTIALS"
    assert mongo_sesh.find_json({"email": email})["is_active"] == 'false'

    # logout_response
    print('\n\n')
    print(response.json())
    print('\n\n')
    print(login_response.json())
    print(logout_response.json())
    print(response.json()["id"])
    print(response.json()["is_active"])
    # print(user["is_active"])
    # print(login_response.json())
    # print(login_response.json())
    print('done')



# def test_logout_non-existing_user():
