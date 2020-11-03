# from fastapi.testclient import TestClient
# from uuid import UUID
# from api.main import app
# from db.mongo import MongoSessionRegular
# import pytest

# test_client = TestClient(app)

# @pytest.fixture(autouse=True)
# def run_around_tests():
#     pytest.login_info = {"username": "parent@hotmail.com", "password": "a!s@d#"}
#     pytest.supply_ids = []
#     yield
#     # Tear Down
#     # Remove supply list data and metadata
#     metadata_sess = MongoSessionRegular(collection="school_supplies_metadata")
#     data_sess = MongoSessionRegular(collection="school_supplies")

#     for id in pytest.supply_ids:
#         metadata_sess.remove_supply_list_metadata(
#             pytest.login_info["username"], UUID(id)
#         )
#         data_sess.remove_supply_list(
#             UUID(id)
#         )
#     metadata_sess.delete_json({"email": pytest.login_info["username"]})


# def test_download_one_list():

#     # Login
#     login_response = test_client.post("/login", data=pytest.login_info)
#     headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

#     # Upload file
#     image_file = open("features/test_files/morris_supply.png", "rb")
#     file_obj = {"file": ("morris_supply.png", image_file, "image/png")}
#     upload_response = test_client.post("/upload", files=file_obj, headers=headers)
#     upload_response_json = upload_response.json()

#     # Add supply list UUID in class variable to get it deleted
#     pytest.supply_ids.append(upload_response_json["school_supply_id"])

#     # Download list
#     download_response = test_client.get("/download", headers=headers)
#     download_response_json = download_response.json()
#     assert download_response.status_code == 200
#     assert download_response_json["Message"] == "Success"
#     assert len(download_response_json["supply_lists"]) == 1
#     assert download_response_json["supply_lists"][0]["id"] == upload_response_json["school_supply_id"]
#     # assert download_response_json["supply_lists"][0]["list_of_supplies"] == [
#     #             "3—1”-1.5” Binders (Must have a binder for each subject)",
#     #             "1 Package of Dividers",
#     #             "1000 Sheets of Looseleaf",
#     #             "8 Duotangs",
#     #             "20 Blue or Black Pens",
#     #             "5 Red Pens",
#     #             "4, Bottles of White-out (Non Toxic)",
#     #             "20 Pencils",
#     #             "4, Erasers",
#     #             "1Pencil Case",
#     #             "1 Box of Kleenex"
#     #         ]
#     assert download_response_json["supply_lists"][0]["original_creator"]["email"] == "parent@hotmail.com"


# def test_download_multiple_lists():
#     # Login
#     login_response = test_client.post("/login", data=pytest.login_info)
#     headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

#     # Upload files
#     image_file_1 = open("features/test_files/morris_supply.png", "rb")
#     file_obj_1 = {"file": ("morris_supply.png", image_file_1, "image/png")}
#     upload_response_1 = test_client.post("/upload", files=file_obj_1, headers=headers)
#     upload_response_json_1 = upload_response_1.json()

#     image_file_2 = open("features/test_files/grade2_supply_list.png", "rb")
#     file_obj_2 = {"file": ("grade2_supply_list.png", image_file_2, "image/png")}
#     upload_response_2 = test_client.post("/upload", files=file_obj_2, headers=headers)
#     upload_response_json_2 = upload_response_2.json()

#     # Download lists
#     download_response = test_client.get("/download", headers=headers)
#     download_response_json = download_response.json()

#     # Add supply list UUIDs in class variable to get them deleted
#     pytest.supply_ids.append(upload_response_json_1["school_supply_id"])
#     pytest.supply_ids.append(upload_response_json_2["school_supply_id"])

#     # Assertions
#     assert download_response.status_code == 200
#     assert download_response_json["Message"] == "Success"
#     assert len(download_response_json["supply_lists"]) == 2
#     assert download_response_json["supply_lists"][0]["id"] == upload_response_json_1["school_supply_id"]
#     # assert download_response_json["supply_lists"][0]["list_of_supplies"] == [
#     #             "3—1”-1.5” Binders (Must have a binder for each subject)",
#     #             "1 Package of Dividers",
#     #             "1000 Sheets of Looseleaf",
#     #             "8 Duotangs",
#     #             "20 Blue or Black Pens",
#     #             "5 Red Pens",
#     #             "4, Bottles of White-out (Non Toxic)",
#     #             "20 Pencils",
#     #             "4, Erasers",
#     #             "1Pencil Case",
#     #             "1 Box of Kleenex"
#     #         ]
#     assert download_response_json["supply_lists"][0]["original_creator"]["email"] == "parent@hotmail.com"
#     assert download_response_json["supply_lists"][1]["id"] == upload_response_json_2["school_supply_id"]
#     # assert download_response_json["supply_lists"][1]["list_of_supplies"] == [
#     #             "1 pencil case: 3 pencils, 1 eraser, 1 pair of scissors, 1 glue stick, 1 sharpener.",
#     #             "3 packs of pencils",
#     #             "7 white erasers",
#     #             "1 sharpener",
#     #             "5 large glue sticks (40g)",
#     #             "1 large white liquid glue",
#     #             "3 boxes of wax crayons (24 per box, all colors needed)",
#     #             "1 pack of markers",
#     #             "3 pocket folders: (no clips) 1 red, 1 green, 1 blue",
#     #             "12 duo-tangs: 3 green, 3 red, 3 blue, 3 orange",
#     #             "2 blue copybooks (30.1 x 21.3)",
#     #             "1 pack of copybooks (pkg of 4)",
#     #             "1 pack of white paper",
#     #             "2x exercise books ¥2 plain and ¥2 lined, blue cover, 40 pages",
#     #             "1 gym uniform (purchased through the school's office)",
#     #             "OPTIONAL",
#     #             "2 packs of paper towel rolls 1 box of large resealable bags",
#     #             "2 boxes of tissue 1 box of small resealable bags",
#     #             "2 boxes of wipes"
#     #         ]
#     assert download_response_json["supply_lists"][1]["original_creator"]["email"] == "parent@hotmail.com"


# def test_download_no_list():
#     # Login
#     login_response = test_client.post("/login", data=pytest.login_info)
#     headers = {"Authorization": "Bearer " + login_response.json()["access_token"]}

#     # Download list
#     download_response = test_client.get("/download", headers=headers)
#     download_response_json = download_response.json()
#     assert download_response.status_code == 400
#     assert download_response_json["detail"] == "No file has been uploaded."