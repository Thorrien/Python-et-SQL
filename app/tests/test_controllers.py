from app.controllers.security import validate_email
import pytest
from unittest.mock import Mock, patch
from app.controllers.control import Controler
from app.dao.userdao import UserDAO
from app.view.views import View 
from app.view.loginview import Loginview 
from app.dao.userdao import UserDAO 
from app.controllers.control import Controler
from app.controllers.login import Login



@pytest.fixture
def mock_view():
    return Mock(spec=View)

@pytest.fixture
def mock_loginview():
    return Mock(spec=Loginview)

@pytest.fixture
def mock_userdao():
    return Mock(spec=UserDAO)


@pytest.fixture
def mock_user():
    user = Mock()
    user.verify_password.return_value = True
    return user


def test_validate_email_valid():
    assert validate_email("bonne@adresse.com") == True

def test_validate_email_invalid():
    assert validate_email("pasadressedutout") == False


def test_login_success(mock_view, mock_loginview, mock_userdao, mock_user):
    mock_userdao.get_user_by_email.return_value = mock_user
    mock_loginview.log.return_value = ("bonne@adresse.com", "correctpassword")

    login = Login()
    login.view = mock_view
    login.loginview = mock_loginview
    login.userdao = mock_userdao

    with patch('app.controllers.login.Controler') as mock_controler_class:
        mock_controler_instance = mock_controler_class.return_value
        login.login()
        mock_view.ascii.assert_called_once()
        mock_loginview.log.assert_called_once()
        mock_userdao.get_user_by_email.assert_called_once_with("bonne@adresse.com")
        mock_user.verify_password.assert_called_once_with("correctpassword")
        mock_loginview.logtrue.assert_called_once()
        mock_controler_class.assert_called_once_with(mock_user, mock_userdao)
        mock_controler_instance.run.assert_called_once()

def test_login_failure_wrong_password(mock_view, mock_loginview, mock_userdao, mock_user):
    mock_userdao.get_user_by_email.return_value = mock_user
    mock_loginview.log.return_value = ("bonne@adresse.com", "wrongpassword")
    mock_user.verify_password.return_value = False

    login = Login()
    login.view = mock_view
    login.loginview = mock_loginview
    login.userdao = mock_userdao

    with patch('builtins.exit') as mock_exit:
        login.login()
        mock_view.ascii.assert_called_once()
        mock_loginview.log.assert_called_once()
        mock_userdao.get_user_by_email.assert_called_once_with("bonne@adresse.com")
        mock_user.verify_password.assert_called_once_with("wrongpassword")
        mock_loginview.logfalse.assert_called_once()
        mock_exit.assert_called_once()

def test_login_failure_unknown_email(mock_view, mock_loginview, mock_userdao):
    mock_userdao.get_user_by_email.return_value = None
    mock_loginview.log.return_value = ("mauvaise@adresse.com", "somepassword")

    login = Login()
    login.view = mock_view
    login.loginview = mock_loginview
    login.userdao = mock_userdao

    with patch('builtins.exit') as mock_exit:
        login.login()
        mock_view.ascii.assert_called_once()
        mock_loginview.log.assert_called_once()
        mock_userdao.get_user_by_email.assert_called_once_with("mauvaise@adresse.com")
        mock_loginview.logfalse.assert_not_called()
        mock_exit.assert_called_once()
