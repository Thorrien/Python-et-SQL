from app.controllers.security import validate_email
import pytest
from unittest.mock import Mock, patch
from app.controllers.control import Controler
from app.dao.userdao import UserDAO


@pytest.fixture(scope='function')
def dao():
    return UserDAO()

@pytest.fixture
def mock_user():
    user = Mock()
    user.id = 1
    user.nom = "BARILLER Eric"
    user.email = "eric.bariller.49@mail.com"
    user.role_id = 1
    user.authorisation = Mock(return_value=True)
    return user


def test_validate_email_valid():
    assert validate_email("test@example.com") == True

def test_validate_email_invalid():
    assert validate_email("pasadressedutout") == False
