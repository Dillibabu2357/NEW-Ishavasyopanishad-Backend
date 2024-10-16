from pprint import pprint

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.management import utils
from app.management.config import settings
from app.management.database import Base, get_db
from app.management.models import User
from app.management.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = settings.test_db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        print("Override override")
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    pprint(app.__dict__)
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_admin(session):
    user_data = {
        "first_name": "Admin",
        "last_name": "Admin",
        "email": "admin@example.com",
        "password": "123",
        "is_admin": True,
    }

    hashed_password = utils.hash_password(user_data["password"])
    user_data["password"] = hashed_password
    new_user = User(**user_data)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    assert new_user.email == user_data["email"]
    assert new_user.first_name == user_data["first_name"]
    assert new_user.last_name == user_data["last_name"]
    assert new_user.is_admin == user_data["is_admin"]

    return new_user


@pytest.fixture
def token_admin(test_admin):
    test_admin = test_admin.__dict__
    return create_access_token(
        {"user_id": test_admin["id"], "is_admin": test_admin["is_admin"]}
    )


@pytest.fixture
def authorized_admin(client, token_admin):
    client.headers = {**client.headers, "Authorization": f"Bearer {token_admin}"}
    yield client


@pytest.fixture
def test_user(client):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@example.com",
        "password": "123",
    }

    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"], "is_admin": "false"})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization 123321": f"Bearer {token}"}
    return client
