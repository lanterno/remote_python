from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_valid_script():
    response = client.post(
        "/execute", json={"script": 'def main():\n    return {"msg": "hello"}'}
    )
    assert response.status_code == 200, response.json()
    assert response.json() == {"msg": "hello"}


def test_script_with_print():
    script = """
def main():
    print("should not be included")
    return {"result": 123}
    """
    response = client.post("/execute", json={"script": script})
    assert response.status_code == 200, response.json()
    assert response.json() == {"result": 123}


def test_missing_main_function():
    script = "def foo(): return {'x':1}"
    response = client.post("/execute", json={"script": script})
    assert response.status_code == 400
    assert "main()" in response.json()["detail"]


def test_syntax_error():
    script = "def main():\n    return { 'x': "
    response = client.post("/execute", json={"script": script})
    assert response.status_code == 400
    assert "Error executing script" in response.json()["detail"]


def test_non_json_return():
    script = "def main():\n    return 'hello'"
    response = client.post("/execute", json={"script": script})
    assert response.status_code == 400
    assert "main() must return a JSON-serializable object" in response.json()["detail"]


def test_empty_request():
    response = client.post("/execute", json={})
    assert response.status_code == 422

    response = client.post("/execute", json={"script": ""})
    assert response.status_code == 400
