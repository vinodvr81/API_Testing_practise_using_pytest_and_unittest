# tests/test_users.py
import pytest
import responses
from src.api_requests import APICheck, BASE_URL

check_req = APICheck()

@pytest.mark.smoke
def test_get_users_one():
    response = check_req.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.regression
def test_create_user_one():
    payload = {
        "name": "Vinod Vukkallam R",
        "email": "vinod.vukkalam_r@example.com",
        "username": "vinodvr"
    }
    response = check_req.post("/users", data=payload)
    assert response.status_code == 201
    assert response.json().get("name") == payload["name"]

@pytest.mark.regression
def test_update_user_one():
    payload = {"name": "Vinod Vukkallam R"}
    response = check_req.put("/users/1", data=payload)
    assert response.status_code == 404
    # assert response.json().get("name") == "Vinod Vukkallam R"

@pytest.mark.regression
def test_delete_user_one():
    response = check_req.delete("/users/1")
    assert response.status_code == 404

@responses.activate
def test_mocked_get_user():
    responses.add(
        responses.GET,
        "http://localhost:3000/users/1",
        json={"id": 1, "name": "Vinod Vukkalam R"},
        status=200
    )

    response = check_req.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Vinod Vukkalam R"

@pytest.mark.smoke
def test_get_all_users():
    response = check_req.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.regression
def test_get_user_by_id():
    response = check_req.get("/users/2")
    assert response.status_code == 200
    assert response.json()["name"] == "Vinod Vukkalam"

@pytest.mark.regression
def test_create_user():
    payload = {
        "id": 2,
        "name": "Vinod Vukkalam",
        "email": "vinod.vukkalam@example.com"
    }
    response = check_req.post("/users", data=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Vinod Vukkalam"

@pytest.mark.regression
def test_update_user():
    payload = {"name": "Vinod Rangaswamy"}
    response = check_req.put("/users/2", data=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Vinod Rangaswamy"

@pytest.mark.regression
def test_delete_user():
    response = check_req.delete("/users/2")
    assert response.status_code == 200

@pytest.mark.negative
def test_get_nonexistent_user():
    response = check_req.get("/users/999")
    assert response.status_code == 404

# @pytest.mark.negative
# def test_create_user_with_invalid_data():
#     payload = {
#         "name": "",  # Invalid: Empty name
#         "email": "invalid-email"
#     }
#     response = check_req.post("/users", data=payload)
#     assert response.status_code == 400  # JSON Server may not strictly enforce validation, but this is good practice

@pytest.mark.boundary
@pytest.mark.parametrize("user_id", [0, -1, 99999999])
def test_get_user_edge_cases(user_id):
    response = check_req.get(f"/users/{user_id}")
    assert response.status_code == 404
