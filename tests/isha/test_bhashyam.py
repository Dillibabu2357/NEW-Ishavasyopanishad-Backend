import pytest 
from fastapi import status

@pytest.fixture
def sutra_data():
    return {"number": 10, "text": "Test Sutra text"}

@pytext.fixture
def 