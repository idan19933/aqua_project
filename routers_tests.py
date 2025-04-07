import requests

BASE_URL = "http://127.0.0.1:5000/users"
EXPEXTED_USERNAMES = ["aviv", "william"]
EXPECTED_USER_INFO = {
    "id": "315520452",
    "phone": "0541234567",
    "name": "aviv",
    "address": "Tel Aviv",
}


def test_list_users():
    print("\nTesting GET /users")
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    usernames = response.json()
    assert isinstance(usernames, list), "Expected a list of usernames"
    assert all(name in usernames for name in EXPEXTED_USERNAMES), (
        "Not all user included"
    )
    print("PASS: Received list of usernames:", usernames)


def test_get_existing_user():
    print("\nTesting GET /users/<existing_user>")
    name = "aviv"
    response = requests.get(f"{BASE_URL}/{name}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    user = response.json()
    assert user == EXPECTED_USER_INFO, "User is not matched."
    print(f"PASS: Retrieved user '{name}' successfully:", user)


def test_get_non_existing_user():
    print("\nTesting GET /users/<non_existing_user>")
    name = "nonexistent"
    response = requests.get(f"{BASE_URL}/{name}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    assert response.json()["error"] == "user not found", "Unexpected error message"
    print(f"PASS: Correctly handled non-existing user '{name}'")


# def test_create_user():
#     print("\nTesting POST /users")
#     payload = {
#         "id": "315520452",
#         "phone": "0541234567",
#         "name": "aviv",
#         "address": "Tel Aviv",
#     }
#     response = requests.post(BASE_URL, json=payload)
#
#     print("Status Code:", response.status_code)
#     print("Response:", response.text)
#
#     assert response.status_code in [201, 400], (
#         f"Unexpected status: {response.status_code}"
#     )
#     print("PASS: User created or already exists.")


if __name__ == "__main__":
    # test_create_user()
    test_list_users()
    test_get_existing_user()
    test_get_non_existing_user()
