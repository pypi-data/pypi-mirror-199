import random
import string

import pytest
from core.contrib.security import PasswordHasher


@pytest.fixture(scope="module")
def password_string():
    strings = string.ascii_letters + string.ascii_uppercase
    return "".join(random.choices(strings, k=12))


def test_password_hashing(password_string):
    hashed_pw = PasswordHasher.hash_password(password_string)

    assert type(hashed_pw) == str
    assert PasswordHasher.verify_password(password_string, hashed_pw)
