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
from app.view.userviews import UserView
from app.view.clientview import ClientView
from datetime import datetime


@pytest.fixture
def mock_view():
    return Mock(spec=View)

@pytest.fixture
def mock_userview():
    return Mock(spec=UserView)

@pytest.fixture
def mock_loginview():
    return Mock(spec=Loginview)

@pytest.fixture
def mock_userdao():
    return Mock(spec=UserDAO)

@pytest.fixture
def mock_clientview():
    return Mock(spec=ClientView)

@pytest.fixture
def mock_user():
    user = Mock()
    user.verify_password.return_value = True
    return user

@pytest.fixture
def mock_controller(mock_user, mock_userdao, mock_view):
    controller = Controler(mock_user, mock_userdao)
    controller.view = mock_view
    return controller


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

def test_run(mock_controller, mock_userdao, mock_view):
    mock_text = Mock()
    mock_text.data = "test"
    mock_userdao.get_text.return_value = mock_text

    with patch.object(mock_controller, 'gestboucle') as mock_gestboucle:
        mock_controller.run()
        mock_userdao.get_text.assert_called_once_with(1)
        mock_view.logtrue.assert_called_once_with(mock_controller.user, "test")
        mock_gestboucle.assert_called_once()


def test_gestboucle(mock_controller, mock_view):
    mock_view.menuprincipalgestion.return_value = "QUIT"
    mock_controller.gestboucle()
    mock_view.menuprincipalgestion.assert_called_once_with(mock_controller.user)

    with patch.object(mock_controller, 'boucleUser', return_value="RET") as mock_boucleUser:
        mock_view.menuprincipalgestion.side_effect = ["US", "QUIT"]
        mock_controller.gestboucle()
        mock_view.menuprincipalgestion.assert_any_call(mock_controller.user)
        mock_boucleUser.assert_called_once()
        
    with patch.object(mock_controller, 'boucleClient', return_value="RET") as mock_boucleClient:
        mock_view.menuprincipalgestion.side_effect = ["CL", "QUIT"]
        mock_controller.gestboucle()
        mock_view.menuprincipalgestion.assert_any_call(mock_controller.user)
        mock_boucleClient.assert_called_once()
        
    with patch.object(mock_controller, 'boucleContracts', return_value="RET") as mock_boucleContracts:
        mock_view.menuprincipalgestion.side_effect = ["CO", "QUIT"]
        mock_controller.gestboucle()
        mock_view.menuprincipalgestion.assert_any_call(mock_controller.user)
        mock_boucleContracts.assert_called_once()
        
    with patch.object(mock_controller, 'boucleEvents', return_value="RET") as mock_boucleEvents:
        mock_view.menuprincipalgestion.side_effect = ["EV", "QUIT"]
        mock_controller.gestboucle()
        mock_view.menuprincipalgestion.assert_any_call(mock_controller.user)
        mock_boucleEvents.assert_called_once()
        
    with patch.object(mock_controller, 'boucleAttributions', return_value="RET") as mock_boucleAttributions:
        mock_view.menuprincipalgestion.side_effect = ["SU", "QUIT"]
        mock_controller.gestboucle()
        mock_view.menuprincipalgestion.assert_any_call(mock_controller.user)
        mock_boucleAttributions.assert_called_once()


def test_boucleUser(mock_controller, mock_user, mock_userdao, mock_userview):
    mock_user.authorisation.side_effect = [True, True]
    mock_userdao.get_all_user_with_role_name.return_value = [
        {'user_id': 1, 'user_name': 'John Doe', 'role_name': 'Admin'},
        {'user_id': 2, 'user_name': 'Jane Doe', 'role_name': 'Gestion'}
    ]
    mock_userview.logutilisateurs.return_value = "RET"
    mock_controller.userview = mock_userview
    with patch('builtins.input', return_value="RET"):
        mock_controller.boucleUser()
    mock_user.authorisation.assert_any_call('Admin')
    mock_userdao.get_all_user_with_role_name.assert_called_once()
    mock_userview.logutilisateurs.assert_called_once_with(mock_user, [
        {'user_id': 1, 'user_name': 'John Doe', 'role_name': 'Admin'},
        {'user_id': 2, 'user_name': 'Jane Doe', 'role_name': 'Gestion'}
    ])
    
def test_main_choice(mock_controller):
    with patch.object(mock_controller, 'create_user') as mock_create_user:
        mock_controller.main_choice('CR')
        mock_create_user.assert_called_once()

    with patch.object(mock_controller, 'handle_user_modification') as mock_handle_user_modification:
        mock_controller.main_choice('A1')
        mock_handle_user_modification.assert_called_once_with('1')
        
    with patch.object(mock_controller, 'handle_user_modification') as mock_handle_user_modification:
        mock_controller.main_choice('M2')
        mock_handle_user_modification.assert_called_once_with('2')
    
    with patch('builtins.quit') as mock_quit:
        mock_controller.main_choice('QUIT')
        mock_quit.assert_called_once()

def test_create_user(mock_controller, mock_userview, mock_userdao):
    mock_userview.createuserview.return_value = ('John Doe', 'john@example.com', 'password123', '1')
    mock_controller.userview = mock_userview
    with patch('builtins.input', side_effect=['John Doe', 'john@example.com', 'password123', '1']):
        mock_controller.create_user()
    mock_userview.createuserview.assert_called_once()
    mock_userdao.add_user.assert_called_once_with('John Doe', 'john@example.com', 'password123', 1)
    
def test_handle_user_modification(mock_controller, mock_user, mock_userdao, mock_userview):
    mock_user_data = Mock(id=1, nom='John Doe', email='john@example.com', role_id=1)
    mock_userdao.get_user.return_value = mock_user_data
    mock_controller.userview = mock_userview

    mock_userview.soloUserView.side_effect = ["SUPPRIMER"]
    mock_controller.handle_user_modification(1)
    mock_userdao.delete_user.assert_called_once_with(1)

    mock_userview.soloUserView.side_effect = ["NO NewName", "RET"]
    mock_controller.handle_user_modification(1)
    mock_userdao.update_user.assert_called_with(1, "NewName", "john@example.com", 1)

    mock_userview.soloUserView.side_effect = ["EM newemail@example.com", "RET"]
    mock_controller.handle_user_modification(1)
    mock_userdao.update_user.assert_called_with(1, "John Doe", "newemail@example.com", 1)

    mock_userview.soloUserView.side_effect = ["SE GE", "RET"]
    mock_controller.handle_user_modification(1)
    mock_userdao.update_user.assert_called_with(1, "John Doe", "john@example.com", 2)
    

def test_boucleClient(mock_controller, mock_user, mock_userdao, mock_clientview):
    mock_user.authorisation.side_effect = [True, True, True, True]
    
    mock_userdao.get_all_company.return_value = [
        {'company_id': 1, 'company_name': 'Company A'},
        {'company_id': 2, 'company_name': 'Company B'}
    ]
    mock_clientview.logclients.side_effect = ["RET"]

    mock_controller.clientview = mock_clientview

    mock_controller.boucleClient()

    mock_user.authorisation.assert_any_call('Admin')
    mock_userdao.get_all_company.assert_called_once()
    mock_clientview.logclients.assert_called_once_with(
        mock_user, 
        [{'company_id': 1, 'company_name': 'Company A'},
         {'company_id': 2, 'company_name': 'Company B'}]
    )
    
def test_client_main_choice(mock_controller):
    with patch.object(mock_controller, 'create_company') as mock_create_company:
        mock_controller.client_main_choice('CR')
        mock_create_company.assert_called_once()

    with patch.object(mock_controller, 'handle_company_modification') as mock_handle_company_modification:
        mock_controller.client_main_choice('A1')
        mock_handle_company_modification.assert_called_once_with('1')
   
    with patch.object(mock_controller, 'handle_company_modification') as mock_handle_company_modification:
        mock_controller.client_main_choice('M2')
        mock_handle_company_modification.assert_called_once_with('2')

    with patch('builtins.quit') as mock_quit:
        mock_controller.client_main_choice('QUIT')
        mock_quit.assert_called_once()
        
def test_process_company_modification_choice(mock_controller):
    mock_company = Mock()
    
    with patch.object(mock_controller, 'create_contact') as mock_create_contact:
        mock_controller.process_company_modification_choice('CR', mock_company, None)
        mock_create_contact.assert_called_once_with(mock_company)
    
    with patch.object(mock_controller, 'recover_company') as mock_recover_company:
        mock_controller.process_company_modification_choice('RECUPERER', mock_company, None)
        mock_recover_company.assert_called_once_with(mock_company)
    
    mock_contacts = Mock()
    
    with patch.object(mock_controller, 'delete_company') as mock_delete_company:
        mock_controller.process_company_modification_choice('SUPPRIMER', mock_company, mock_contacts)
        mock_delete_company.assert_called_once_with(mock_company, mock_contacts)
    
    with patch.object(mock_controller, 'update_company_name') as mock_update_company_name:
        mock_controller.process_company_modification_choice('MN Nouvelle Entreprise', mock_company, None)
        mock_update_company_name.assert_called_once_with(mock_company, 'Nouvelle Entreprise')

    with patch.object(mock_controller, 'update_company_address') as mock_update_company_address:
        mock_controller.process_company_modification_choice('MA Nouvelle Adresse', mock_company, None)
        mock_update_company_address.assert_called_once_with(mock_company, 'Nouvelle Adresse')

    with patch.object(mock_controller, 'handle_contact_modification') as mock_handle_contact_modification:
        mock_controller.process_company_modification_choice('A1', mock_company, None)
        mock_handle_contact_modification.assert_called_once_with('1', mock_company)
        
    with patch('builtins.quit') as mock_quit:
        mock_controller.process_company_modification_choice('QUIT', None, None)
        mock_quit.assert_called_once()

    with patch('builtins.print') as mock_print:
        mock_controller.process_company_modification_choice('UNKNOWN', mock_company, None)
        mock_print.assert_called_once_with("commande inconnue")
        
def test_process_contact_modification(mock_controller):
    mock_contact = Mock(id=1, name='John Doe', email='email@example.com', phone='1234567890', signatory=0)
    mock_company = Mock(id=1)

    with patch.object(mock_controller.userDAO, 'delete_contact') as mock_delete_contact:
        mock_controller.process_contact_modification_choice('SUPPRIMER', mock_contact, mock_company)
        mock_delete_contact.assert_called_once_with(1)
    
    with patch.object(mock_controller.userDAO, 'update_contact') as mock_update_contact:
        mock_controller.process_contact_modification_choice('NO New Name', mock_contact, mock_company)
        mock_update_contact.assert_called_once_with(1, 1, 'New Name', 'email@example.com', '1234567890', 0)

    mock_contact.name = 'John Doe'

    with patch.object(mock_controller.userDAO, 'update_contact') as mock_update_contact:
        mock_controller.process_contact_modification_choice('EM newemail@example.com', mock_contact, mock_company)
        mock_update_contact.assert_called_once_with(1, 1, 'John Doe', 'newemail@example.com', '1234567890', 0)

    mock_contact.name = 'John Doe'

    with patch.object(mock_controller.userDAO, 'update_contact') as mock_update_contact:
        mock_controller.process_contact_modification_choice('TE 0987654321', mock_contact, mock_company)
        mock_update_contact.assert_called_once_with(1, 1, 'John Doe', 'email@example.com', '0987654321', 0)

    mock_contact.name = 'John Doe'

    with patch.object(mock_controller.userDAO, 'update_contact') as mock_update_contact:
        mock_controller.process_contact_modification_choice('SI Oui', mock_contact, mock_company)
        mock_update_contact.assert_called_once_with(1, 1, 'John Doe', 'email@example.com', '1234567890', 1)

    mock_contact.name = 'John Doe'

    with patch.object(mock_controller.userDAO, 'update_contact') as mock_update_contact:
        mock_controller.process_contact_modification_choice('SI Non', mock_contact, mock_company)
        mock_update_contact.assert_called_once_with(1, 1, 'John Doe', 'email@example.com', '1234567890', 0)

    with patch('builtins.quit') as mock_quit:
        mock_controller.process_contact_modification_choice('QUIT', None, None)
        mock_quit.assert_called_once()

    with patch('builtins.print') as mock_print:
        mock_controller.process_contact_modification_choice('UNKNOWN', mock_contact, mock_company)
        mock_print.assert_any_call("commande inconnue")
        
def test_handle_main_choice(mock_controller):
    mock_contrats = Mock()
    mock_supports = Mock()

    with patch.object(mock_controller, 'create_contract') as mock_create_contract:
        mock_controller.handle_main_choice("CR123", mock_contrats, mock_supports)
        mock_create_contract.assert_called_once_with("CR123")

    with patch.object(mock_controller, 'view_contract') as mock_view_contract:
        mock_controller.handle_main_choice("A456", mock_contrats, mock_supports)
        mock_view_contract.assert_called_once_with("A456", mock_contrats, mock_supports)

    with patch.object(mock_controller, 'view_company') as mock_view_company:
        mock_controller.handle_main_choice("E789", mock_contrats, mock_supports)
        mock_view_company.assert_called_once_with("E789")

    with patch.object(mock_controller, 'delete_contract') as mock_delete_contract:
        mock_controller.handle_main_choice("S101", mock_contrats, mock_supports)
        mock_delete_contract.assert_called_once_with("S101", mock_contrats)

    with patch('builtins.quit') as mock_quit:
        mock_controller.handle_main_choice("QUIT", mock_contrats, mock_supports)
        mock_quit.assert_called_once()
        
        
def test_contract_choice(mock_controller):
    mock_contrat = Mock()
    mock_company = Mock()
    mock_events = Mock()
    mock_supports = Mock()

    with patch.object(mock_controller, 'view_event') as mock_view_event:
        mock_controller.contract_choice("A123", mock_contrat, mock_company, mock_events, mock_supports)
        mock_view_event.assert_called_once_with("A123")

    with patch.object(mock_controller, 'create_event') as mock_create_event:
        mock_controller.contract_choice("CR", mock_contrat, mock_company, mock_events, mock_supports)
        mock_create_event.assert_called_once_with(mock_company, mock_contrat, mock_supports)

    with patch.object(mock_controller, 'delete_contract_if_authorized') as mock_delete_contract:
        result = mock_controller.contract_choice("SUPPRIMER", mock_contrat, mock_company, mock_events, mock_supports)
        mock_delete_contract.assert_called_once_with(mock_contrat, mock_company)
        assert result == 'LIST'

    with patch.object(mock_controller, 'update_contract_total') as mock_update_contract_total:
        mock_controller.contract_choice("MT 5000", mock_contrat, mock_company, mock_events, mock_supports)
        mock_update_contract_total.assert_called_once_with("MT 5000", mock_contrat, mock_company)

    with patch.object(mock_controller, 'update_contract_current') as mock_update_contract_current:
        mock_controller.contract_choice("MV 2500", mock_contrat, mock_company, mock_events, mock_supports)
        mock_update_contract_current.assert_called_once_with("MV 2500", mock_contrat, mock_company)

    with patch.object(mock_controller, 'update_contract_sign') as mock_update_contract_sign:
        mock_controller.contract_choice("MS SI", mock_contrat, mock_company, mock_events, mock_supports)
        mock_update_contract_sign.assert_called_once_with(mock_contrat, mock_company, sign=1)

    with patch.object(mock_controller, 'update_contract_sign') as mock_update_contract_sign:
        mock_controller.contract_choice("MS NS", mock_contrat, mock_company, mock_events, mock_supports)
        mock_update_contract_sign.assert_called_once_with(mock_contrat, mock_company, sign=0)

    result = mock_controller.contract_choice("RET", mock_contrat, mock_company, mock_events, mock_supports)
    assert result == "RET"

    with patch('builtins.quit') as mock_quit:
        mock_controller.contract_choice("QUIT", mock_contrat, mock_company, mock_events, mock_supports)
        mock_quit.assert_called_once()
        
def test_event_choice(mock_controller):
    mock_event = Mock(id=1, event_date_start=datetime(2024, 8, 19, 10, 0), 
                      event_date_end=datetime(2024, 8, 19, 12, 0),
                      location="Paris", id_user=42, attendees=100, notes="Meeting")

    with patch.object(mock_controller.userDAO, 'delete_event') as mock_delete_event:
        result = mock_controller.event_choice("SUPPRIMER", mock_event)
        mock_delete_event.assert_called_once_with(1)
        assert result == 'LIST'

    result = mock_controller.event_choice("RET", mock_event)
    assert result == "RET"

    with patch('builtins.quit') as mock_quit:
        mock_controller.event_choice("QUIT", mock_event)
        mock_quit.assert_called_once()

    with patch.object(mock_controller.userDAO, 'update_event') as mock_update_event:
        mock_controller.event_choice("MS 19/08/2024 15:00", mock_event)
        mock_update_event.assert_called_once_with(
            1, datetime(2024, 8, 19, 15, 0), 
            mock_event.event_date_end, 
            mock_event.location, 
            mock_event.id_user, 
            mock_event.attendees, 
            mock_event.notes
        )

    with patch.object(mock_controller.userDAO, 'update_event') as mock_update_event:
        mock_controller.event_choice("ME 19/08/2024 18:00", mock_event)
        mock_update_event.assert_called_once_with(
            1, mock_event.event_date_start, 
            datetime(2024, 8, 19, 18, 0), 
            mock_event.location, 
            mock_event.id_user, 
            mock_event.attendees, 
            mock_event.notes
        )

    with patch.object(mock_controller.userDAO, 'update_event') as mock_update_event:
        mock_controller.event_choice("ML New Location", mock_event)
        mock_update_event.assert_called_once_with(
            1, mock_event.event_date_start, 
            mock_event.event_date_end, 
            "New Location", 
            mock_event.id_user, 
            mock_event.attendees, 
            mock_event.notes
        )

    with patch.object(mock_controller.userDAO, 'update_event') as mock_update_event:
        mock_controller.event_choice("MA 150", mock_event)
        mock_update_event.assert_called_once_with(
            1, mock_event.event_date_start, 
            mock_event.event_date_end, 
            mock_event.location, 
            mock_event.id_user, 
            "150", 
            mock_event.notes
        )

    with patch.object(mock_controller.userDAO, 'update_event') as mock_update_event:
        mock_controller.event_choice("MN Updated notes", mock_event)
        mock_update_event.assert_called_once_with(
            1, mock_event.event_date_start, 
            mock_event.event_date_end, 
            mock_event.location, 
            mock_event.id_user, 
            mock_event.attendees, 
            "Updated notes"
        )

def test_boucleSoloEvents(mock_controller):
    mock_event = Mock(id=1, event_date_start=datetime(2024, 8, 19, 10, 0), 
                      event_date_end=datetime(2024, 8, 19, 12, 0),
                      location="Paris", id_user=42, attendees=100, notes="Meeting")
    
    mock_controller.userDAO.get_event.return_value = mock_event
    
    with patch.object(mock_controller.eventview, 'eventview', side_effect=["SUPPRIMER", "RET", "QUIT"]):
        with patch.object(mock_controller.userDAO, 'delete_event') as mock_delete_event:
            result = mock_controller.boucleSoloEvents("A1")
            mock_delete_event.assert_called_once_with(1)
            assert result == 'LIST'
    
    with patch.object(mock_controller.eventview, 'eventview', side_effect=["RET"]):
        result = mock_controller.boucleSoloEvents("A1")
        assert result == "RET"

    with patch('builtins.quit') as mock_quit:
        with patch.object(mock_controller.eventview, 'eventview', side_effect=["QUIT"]):
            mock_controller.boucleSoloEvents("A1")
            mock_quit.assert_called_once()

def test_handle_events_choice(mock_controller):
    mock_events = [Mock(id=1), Mock(id=2)]

    with patch.object(mock_controller, 'handle_total_events_choice') as mock_handle_total:
        mock_controller.handle_events_choice("TO", mock_events)
        mock_handle_total.assert_called_once_with(mock_events)

    with patch.object(mock_controller, 'handle_total_events_choice') as mock_handle_total:
        mock_controller.handle_events_choice("TT", mock_events)
        mock_handle_total.assert_called_once_with(mock_events)

    with patch.object(mock_controller, 'boucleSoloEvents') as mock_boucle_solo:
        mock_controller.handle_events_choice("A1", mock_events)
        mock_boucle_solo.assert_called_once_with("A1")

    result = mock_controller.handle_events_choice("UNKNOWN", mock_events)
    assert result == "UNKNOWN"
    
def test_handle_total_events_choice(mock_controller):
    mock_events = [Mock(id=1), Mock(id=2)]

    with patch.object(mock_controller.eventview, 'myTotalEvents', side_effect=["A1", "RET"]):
        with patch.object(mock_controller, 'boucleSoloEvents') as mock_boucle_solo:
            result = mock_controller.handle_total_events_choice(mock_events)
            mock_boucle_solo.assert_called_once_with("A1")
            assert result == "RET"

    with patch.object(mock_controller.eventview, 'myTotalEvents', side_effect=["TT", "RET"]):
        with patch.object(mock_controller, 'handle_tt_events_choice') as mock_handle_tt:
            result = mock_controller.handle_total_events_choice(mock_events)
            mock_handle_tt.assert_called_once_with(mock_events)
            assert result == "RET"

    with patch.object(mock_controller.eventview, 'myTotalEvents', side_effect=["UNKNOWN", "RET"]):
        result = mock_controller.handle_total_events_choice(mock_events)
        assert result == "UNKNOWN"
        
def test_handle_tt_events_choice(mock_controller):
    mock_events = [Mock(id=1), Mock(id=2)]

    with patch.object(mock_controller.eventview, 'TotalEvents', side_effect=["A1", "RET"]):
        with patch.object(mock_controller, 'boucleSoloEvents') as mock_boucle_solo:
            result = mock_controller.handle_tt_events_choice(mock_events)
            mock_boucle_solo.assert_called_once_with("A1")
            assert result == "RET"

    with patch.object(mock_controller.eventview, 'TotalEvents', side_effect=["UNKNOWN", "RET"]):
        result = mock_controller.handle_tt_events_choice(mock_events)
        assert result == "UNKNOWN"