from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_register_user():
    response = client.post("/register")

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

    assert response.status_code == 201


def test_register_existing_user():
    # dummy test user
    email = "testingemail@preexisting.com"
    password = "testingpassword"

    # add user in case not existing
    response = client.post("/register", json={
        "email": email,
        "password": password
    })

    # add the same user again
    response = client.post("/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "REGISTER_USER_ALREADY_EXISTS"}

    # TODO: remove the user from the database before ending this test
