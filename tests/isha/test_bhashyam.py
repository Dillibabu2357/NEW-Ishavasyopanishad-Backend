import pytest
from fastapi import status


@pytest.fixture
def sutra_data():
    return {"number": 10, "text": "Test Sutra text"}


@pytest.fixture
def bhashyam_data():
    return {
        "language": "sa",
        "text": "Test interpretation text",
        "philosophy": "adv",
    }


@pytest.mark.parametrize(
    "client_type",
    [
        "client",
        "authorized_client",
        "authorized_admin",
    ],
)
def test_get_bhashyam(
    client_type,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    bhashyam_data,
):
    # Create Sutra
    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Add Bhashyam
    response = authorized_admin.post(
        f"/isha/sutras/{sutra_data['number']}/bhashyam",
        json=bhashyam_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Client selection
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    # Get Bhashyam
    response = test_client.get(
        f"/isha/sutras/{sutra_data['number']}/bhashyam?lang={bhashyam_data['language']}&phil={bhashyam_data['philosophy']}",
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK

    # Ensure the bhashyam data returned matches the created data
    bhashyam_data["sutra_id"] = 1  # Assuming the id is assigned by the server
    assert response.json() == bhashyam_data


@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        (
            "client",
            status.HTTP_401_UNAUTHORIZED,
        ),  # Unauthorized client should return 401
        (
            "authorized_client",
            status.HTTP_201_CREATED,
        ),  # Authorized regular user should return 201
        (
            "authorized_admin",
            status.HTTP_201_CREATED,
        ),  # Authorized admin should also return 201
    ],
)
def test_add_bhashyam(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    bhashyam_data,
):
    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    response = test_client.post(
        f"/isha/sutras/{sutra_data['number']}/bhashyam",
        json=bhashyam_data,
    )
    print(response.json())
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        (
            "client",
            status.HTTP_401_UNAUTHORIZED,
        ),  # Unauthorized client should return 401
        (
            "authorized_client",
            status.HTTP_204_NO_CONTENT,
        ),  # Authorized regular user should return 204
        (
            "authorized_admin",
            status.HTTP_204_NO_CONTENT,
        ),  # Authorized admin should also return 204
    ],
)
def test_update_bhashyam(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    bhashyam_data,
):

    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = authorized_admin.post(
        f"/isha/sutras/{sutra_data['number']}/bhashyam",
        json=bhashyam_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    updated_bhashyam = {
        "language": "sa",
        "text": "Test updated interpretation text",
        "philosophy": "adv",
    }

    response = test_client.put(
        f"/isha/sutras/{sutra_data['number']}/bhashyam?lang={bhashyam_data['language']}&phil={bhashyam_data['philosophy']}",
        json=updated_bhashyam,
    )
    print(response.content)  # This shows the raw content of the response

    # Check if the response has content to parse as JSON
    if response.content:
        print(response.json())  # Parse as JSON if content exists
    else:
        print("No content returned, skipping JSON parsing.")

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_204_NO_CONTENT:
        response = test_client.get(
            f"/isha/sutras/{sutra_data['number']}/bhashyam?lang={updated_bhashyam['language']}"
        )
        assert response.status_code == status.HTTP_200_OK
        updated_bhashyam["sutra_id"] = 1
        assert response.json() == updated_bhashyam



@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        (
            "client",
            status.HTTP_401_UNAUTHORIZED,
        ),  # Unauthorized client should return 401
        (
            "authorized_client",
            status.HTTP_403_FORBIDDEN,
        ),  # Authorized regular user should return 403
        (
            "authorized_admin",
            status.HTTP_204_NO_CONTENT,
        ),  # Authorized admin should return 204
    ],
)
def test_delete_bhashyam(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    bhashyam_data,
):
    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = authorized_admin.post(
        f"/isha/sutras/{sutra_data['number']}/bhashyam",
        json=bhashyam_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]
    response = test_client.delete(
        f"/isha/sutras/{sutra_data['number']}/bhashyam?lang={bhashyam_data['language']}&phil={bhashyam_data['philosophy']}"
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")

    if response.status_code == 204:
        print("No content returned as expected.")
    else:
        print(response.json())

    assert response.status_code == expected_status
