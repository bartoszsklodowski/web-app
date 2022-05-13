import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("name", ['Zenek', 'Marek', 'Alojzy Niezdąży'])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert f"Hello {name}" in response.text
