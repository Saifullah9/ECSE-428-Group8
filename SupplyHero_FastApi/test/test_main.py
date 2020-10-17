from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# Test template from the documentation: TODO remove
def test_template():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }
