from fastapi.testclient import TestClient
import random
from api.main import app

client = TestClient(app)

# test registering a new user, loggin them in, and then loggiing out the account PERMANENTLY
def test_logout_user():
    rando = random.randint(1, 50000000)
    email = "usertest" + str(rando) + "@example.com"
    password = "string"

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
    # assert response.status_code == 422

    # login_response = client.post("/login", json={"id": response.json()['id'], "email": email, "password": password})
    # # assert login was success
    # assert login_response.json() != {
    #     "detail": "LOGIN_BAD_CREDENTIALS"
    # }
    # verify user is currently active
    assert response.json()["is_active"] == True
    logout_response = client.post("logout")
    print(logout_response.json())
    # logout_response
    print('\n\n')
    print(response.json())
    print('\n\n')
    print(response.json()["id"])
    print(response.json()["is_active"])

    # print(login_response.json())

    # print(login_response.json())
    print('done')



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