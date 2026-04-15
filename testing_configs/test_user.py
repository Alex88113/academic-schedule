import pytest

class User:
    def __init__(self, age: int, name: str) -> None:
        self.age = age
        self.name = name

    def is_adult(self) -> bool:
        if self.age < 18:
            return False
        return True

    def processing_name(self) -> str:
        processing: str = self.name.strip().lower().capitalize()
        return processing


@pytest.fixture
def user1():
    user =  User("Shura", 10)
    return user

def test_user1(user1):
    assert user1.processing_name() == "Shura"
