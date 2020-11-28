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
    assert delete_list_response.status_code == 200
    print('done')



# def test_logout_non-existing_user():
