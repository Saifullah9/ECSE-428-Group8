from fastapi.testclient import TestClient
from db.mongo import MongoSessionRegular

import random
import json
from api.main import app
import uuid
client = TestClient(app)
mongo_sesh = MongoSessionRegular(collection='users')
metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
data_sess = MongoSessionRegular(collection="school_supplies")
# tests the functionality of the delete
def test_delete_list_in_user():
    #this is the relevant creation of the id, and attempt to remove it after
    uuid_temp = uuid.uuid4()
    metadata_sess.upsert_supply_list_metadata_email("myemail@gmail.com", uuid_temp)
    # stringer = str(uuid_temp)
    #trying to remove uuid
    # delete_list_response = client.delete("/List", data={"supply_list_id" : uuid_temp, "email": "myemail@gmail.com"})
    delete_list_response = client.delete("/List?supply_list_id=" + str(uuid_temp) + "&email=myemail%40gmail.com")
    assert json.loads(delete_list_response.content)["Message"] == "Success, id has been removed"
    # metadata_sess.remove_supply_list_metadata("myemail@gmail.com", uuid_temp) #backup that will deffinitely remove uuuid so they dont pile up

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
    image_file = open("../features/test_files/morris_supply.png", "rb")
    file_obj = {"file": ("morris_supply.png", image_file, "image/png")}

    upload_response = client.post("/upload", files=file_obj, headers=headers)

    delete_list_user = client.delete("/ListLogin?Authorization=Bearer" + jwt_token + "&supply_list_id=" + str(json.loads(upload_response.content)["school_supply_id"]), headers=headers)
    # assert delete_list_user.content

    print('done')



# def test_logout_non-existing_user():
