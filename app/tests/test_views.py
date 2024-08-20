import pytest, datetime
from app.view.views import View
from app.view.userviews import UserView
from unittest.mock import Mock, patch
from app.dao.userdao import UserDAO
from app.view.loginview import Loginview
from app.controllers.security import validate_email
from app.view.eventview import EventView
from app.view.contractview import ContractView
from app.view.clientview import ClientView

@pytest.fixture
def mock_user():
    user = Mock()
    user.email = "eric@gmail.com"
    user.nom = "Eric BARILLER"
    user.authorisation.return_value = True  
    return user

@pytest.fixture
def mock_contact():
    contact = Mock()
    contact.email = "eric@gmail.com"
    contact.nom = "Eric BARILLER"
    contact.phone = "0123456789"
    contact.id = 1
    contact.signatory = 1
    contact.creation_date = datetime.datetime(2024, 8, 1, 10, 0, 0)
    contact.update_date = datetime.datetime(2024, 8, 10, 10, 0, 0)
    return contact

@pytest.fixture
def mock_affiche():
    affiche = Mock()
    affiche.id = 1
    affiche.nom = "Alice"
    affiche.email = "alice@example.com"
    affiche.role_id = "Admin"
    affiche.date_creation = "01/01/2021"
    return affiche

@pytest.fixture
def mock_events():
    event1 = Mock()
    event1.id = 1
    event1.attendees = 10
    event1.location = "Angers"
    event1.event_date_start = datetime.datetime(2024, 8, 19, 10, 0, 0)
    event1.event_date_end = datetime.datetime(2024, 8, 19, 12, 0, 0)
    event1.event_date_end_str = event1.event_date_end.strftime("%Y-%m-%d %H:%M:%S")

    event2 = Mock()
    event2.id = 2
    event2.location = "Paris"
    event2.attendees = 20
    event2.event_date_start = datetime.datetime(2024, 8, 19, 10, 0, 0)
    event2.event_date_end = datetime.datetime(2024, 8, 19, 12, 0, 0)
    event2.event_date_end_str = event2.event_date_end.strftime("%Y-%m-%d %H:%M:%S")

    return [event1, event2]

@pytest.fixture
def mock_company():
    company = Mock()
    company.user_id = 1
    company.company_name = "Total"
    return company

@pytest.fixture
def mock_contrat():
    contrat = Mock()
    contrat.id = 1
    contrat.user_id = 1
    contrat.total_amont = 10000
    contrat.current_amont = 5000
    contrat.creation_date = datetime.datetime(2024, 8, 1, 10, 0, 0)
    contrat.update_date = datetime.datetime(2024, 8, 10, 10, 0, 0)
    contrat.sign = True
    return contrat

@pytest.fixture
def mock_contracts():
    contrat1 = Mock()
    contrat1.id = 1
    contrat1.compagny_id = 1
    contrat1.user_id = 1
    contrat1.total_amont = 15000
    contrat1.current_amont = 100
    contrat1.sign = 1

    contrat2 = Mock()
    contrat2.id = 2
    contrat2.compagny_id = 1
    contrat2.user_id = 1
    contrat2.total_amont = 150000
    contrat2.current_amont = 10000
    contrat2.sign = 0
    
    return [contrat1, contrat2]


@pytest.fixture
def mock_events2():
    event1 = {
        'event_id': 1,
        'attendees': 10,
        'id_user' : 1,
        'event_date_start': datetime.datetime(2024, 8, 19, 10, 0, 0),
        'event_date_end': datetime.datetime(2024, 8, 19, 12, 0, 0),
        'location': 'Location A',
        'notes': 'Event in August',
        'company_name': 'Truc et astuces'
    }

    event2 = {
        'event_id': 2,
        'attendees': 20,
        'id_user' : 1,
        'event_date_start': datetime.datetime(2024, 9, 1, 14, 0, 0),
        'event_date_end': datetime.datetime(2024, 9, 1, 16, 0, 0),
        'location': 'Location B',
        'notes': 'Event in September',
        'company_name': 'Truc et astuces'
    }
    
    event3 = {
        'event_id': 3,
        'attendees': 200,
        'id_user' : 1,
        'event_date_start': datetime.datetime(2024, 9, 1, 14, 0, 0),
        'event_date_end': datetime.datetime(2024, 9, 1, 16, 0, 0),
        'location': 'Location B',
        'notes': 'Event in September',
        'company_name': 'Truc et astuces'
    }
    return [event1, event2, event3]

@pytest.fixture
def mock_companys():
    company1 = Mock()
    company1.id = 1
    company1.company_name = "Total"
    company1.address = "56 rue de l'avenir"
    company1.update_date = datetime.datetime(2024, 8, 19, 10, 0, 0)
    company1.update_date_str = company1.update_date.strftime("%Y-%m-%d %H:%M:%S")

    company2 = Mock()
    company2.id = 2
    company2.company_name = "NASA"
    company2.address = "56 rue de l'avenir lointain"
    company2.update_date = datetime.datetime(2024, 8, 19, 10, 0, 0)
    company2.update_date_str = company1.update_date.strftime("%Y-%m-%d %H:%M:%S")

    return [company1, company2]

@pytest.fixture
def mock_users():
    user1 = Mock()
    user1.id = 1
    user1.nom = "Alice"
    user1.email = "alice@example.com"

    user2 = Mock()
    user2.id = 2
    user2.nom = "Bob"
    user2.email = "bob@example.com"

    return [user1, user2]

@pytest.fixture
def mock_event():
    event = Mock()
    event.id = 1
    event.id_user = 1
    event.event_date_start = datetime.datetime(2024, 8, 19, 10, 0, 0)
    event.event_date_end = datetime.datetime(2024, 8, 19, 12, 0, 0)
    event.location = "TOTAL"
    event.attendees = 50
    event.notes = "Some notes"
    return event

@pytest.fixture
def mock_contacts():
    contact1 = Mock()
    contact1.id = 1
    contact1.name = "John Doe"
    contact1.email = "john@Doe.com"
    contact1.phone = "0123456789"
    contact1.signatory = True
    contact1.update_date = datetime.datetime(2024, 8, 18, 9, 0, 0)
    contact1.update_date_str = contact1.update_date.strftime("%Y-%m-%d %H:%M:%S")

    contact2 = Mock()
    contact2.id = 2
    contact2.name = "Jane Doe"
    contact2.email = "jane@Doe.com"
    contact2.phone = "0123456789"
    contact2.signatory = False
    contact2.update_date = datetime.datetime(2024, 8, 18, 10, 0, 0)
    contact2.update_date_str = contact2.update_date.strftime("%Y-%m-%d %H:%M:%S")

    return [contact1, contact2]

@pytest.fixture
def mock_userdao():
    userdao = Mock()
    userdao.get_user.return_value = Mock(nom="Other User")
    return userdao


def test_ascii_output(capfd):
    view = View()
    view.ascii()

    element = capfd.readouterr()
    expected_substring = "___           ___                     ___"
    
    assert expected_substring in element.out


def test_title_output(capfd, mock_user):
    view = View()
    view.title(mock_user)

    element = capfd.readouterr()

    expected_email = f"{mock_user.email}"

    assert expected_email in element.out

def test_title_output(capfd, mock_user):
    view = View()
    view.logtrue(mock_user, "message test")

    element = capfd.readouterr()

    expected_nom = f"{mock_user.nom}"
    expected_message = "message test"
    assert expected_nom in element.out
    assert expected_message in element.out

def test_menuprincipalgestion_output(capfd, mock_user):
    view = View()
    mock_user.authorisation.side_effect = lambda role: role in ['Admin']
    
    with patch('builtins.input', return_value='QUIT'):
        view.menuprincipalgestion(mock_user)

    element = capfd.readouterr()
    assert "Gérer les comptes utilisateurs" in element.out
    assert "Gérer les clients" in element.out
    assert "Gérer les contrats" in element.out
    assert "Gérer les Events" in element.out

def test_base_output(capfd):
    view = View()
    view.base()

    element = capfd.readouterr()
    
    assert "Fin de la page" in element.out
    
def test_notautorized_output(capfd, mock_user):
    view = View()
    view.notautorized(mock_user)

    element = capfd.readouterr()
    
    assert "vous n'avez pas les droits" in element.out
    
def test_logutilisateurs_output(capfd, mock_user):
    userview = UserView()
    dao = Mock(spec=UserDAO)
    
    dao.get_all_users.return_value = [
        {'user_id': 1, 'user_name': 'Alice', 'role_name': 'Admin'},
        {'user_id': 2, 'user_name': 'Bob', 'role_name': 'User'},
        {'user_id': 3, 'user_name': 'Charlie', 'role_name': 'Manager'},
    ]
     
    with patch('builtins.input', return_value='RET'):
        userview.logutilisateurs(mock_user, dao.get_all_users())

    element = capfd.readouterr()
    
    assert "Alice" in element.out
    assert "Créer un nouvel utilisateur" in element.out
    assert "Afficher le détail d'un utilisateur <id>" in element.out
    assert "Modifier un élément d'un utilisateur <id>" in element.out

def test_soloUserView_output(capfd, mock_user, mock_affiche):
    userview = UserView()
    
    with patch('builtins.input', return_value='RET'):
        userview.soloUserView(mock_user, mock_affiche)

    element = capfd.readouterr()

    assert "Alice" in element.out
    assert "alice@example.com" in element.out
    assert "Admin" in element.out
    assert "Supprime définitivement l'utilisateur" in element.out
    assert "Retour au menu précédent" in element.out
    assert "quitter l'application" in element.out
    
def test_logWithoutUser_output(capfd, mock_user, mock_events, mock_companys):
    userview = UserView()

    with patch('builtins.input', return_value='RET'):
        userview.logWithoutUser(mock_user, mock_events, mock_companys)

    element = capfd.readouterr()

    assert "Détail de tous les éléments non attribués" in element.out
    assert "Evènements" in element.out
    assert "Entreprises" in element.out

    for event in mock_events:
        assert str(event.id) in element.out
        assert str(event.attendees) in element.out
        assert event.event_date_start.strftime("%Y-%m-%d %H:%M:%S") in element.out

    for company in mock_companys:
        assert str(company.id) in element.out
        assert company.company_name in element.out

    assert "Attribuer l'évènement" in element.out
    assert "Attribuer l'entreprise" in element.out
    assert "Retour au menu précédent" in element.out
    assert "Quitter le programme" in element.out

def test_chooseUser_output(capfd, mock_users):
    userview = UserView()

    with patch('builtins.input', return_value='RET'):
        userview.chooseUser(mock_users)

    element = capfd.readouterr()

    assert "Liste des persones correpondantes" in element.out
    assert "Utilisateurs" in element.out

    for user in mock_users:
        assert str(user.id) in element.out
        assert user.nom in element.out
        assert user.email in element.out


    assert "Attribuer l'évènement a <id>" in element.out
    assert "Retour au menu précédent" in element.out
    assert "Quitter le programme" in element.out

def test_log_valid_email(capfd):
    loginview = Loginview()

    with patch('builtins.input', side_effect=['bonne@adresse.com']):
        with patch('getpass.getpass', return_value='securepassword'):
            with patch('app.controllers.security.validate_email', return_value=True):
                email, password = loginview.log()
                
                element = capfd.readouterr()
                assert "Quel est votre Identifiant ?" in element.out
                assert email == 'bonne@adresse.com'
                assert password == 'securepassword'

def test_log_invalid_email(capfd):
    loginview = Loginview()

    with patch('builtins.input', return_value='invalidemail'):
        with patch('app.controllers.security.validate_email', return_value=False):
            with patch('builtins.exit') as mock_exit:
                loginview.log()
                element = capfd.readouterr()
                assert "format d'email invalide" in element.out
                mock_exit.assert_called_once()

def test_eventview_with_authorization(capfd, mock_user, mock_event, mock_userdao):
    eventview = EventView()

    with patch('builtins.input', return_value='RET'):
        eventview.eventview(mock_user, mock_event, mock_userdao)

    element = capfd.readouterr()

    assert "Gestionnaire" in element.out
    assert "Date de début" in element.out
    assert "RET" in element.out

def test_myMensualEvents_current_month(capfd, mock_user, mock_events2):
    eventview = EventView()

    with patch('builtins.input', return_value='RET'):
        eventview.myMensualEvents(mock_user, mock_events2)

    element = capfd.readouterr()


    assert "Détail des évènements du mois" in element.out
    assert "10" in element.out  

def test_myMensualEvents_next_month(capfd, mock_user, mock_events2):
    eventview = EventView()

    with patch('builtins.input', return_value='RET'):
        eventview.myMensualEvents(mock_user, mock_events2)

    element = capfd.readouterr()


    assert "Détail des évènements du mois" in element.out
    assert "20" in element.out 
    
    
def test_myTotalEvents_next_month(capfd, mock_user, mock_events2):
    eventview = EventView()

    with patch('builtins.input', return_value='RET'):
        eventview.myTotalEvents(mock_user, mock_events2)

    element = capfd.readouterr()


    assert "Détail de tous vos évènements" in element.out
    assert "Votre choix" in element.out 
    
def test_TotalEvents_next_month(capfd, mock_user, mock_events2):
    eventview = EventView()

    with patch('builtins.input', return_value='RET'):
        eventview.TotalEvents(mock_user, mock_events2)

    element = capfd.readouterr()


    assert "Détail de tous les évènements" in element.out
    assert "Votre choix" in element.out 

def test_logcontrats(capfd, mock_user, mock_userdao, mock_contracts):
    eventcontract = ContractView()

    with patch('builtins.input', return_value='RET'):
        eventcontract.logcontracts(mock_user, mock_contracts, mock_userdao)

    element = capfd.readouterr()

    assert "Contrats" in element.out
    assert "Suprimer définitivement le contrat" in element.out 
    
def test_contractview(capfd, mock_user, mock_company, mock_contrat, mock_events, mock_userdao):
    eventcontract = ContractView()

    with patch('builtins.input', return_value='RET'):
        eventcontract.contractview(mock_user, mock_company, mock_contrat, mock_events, mock_userdao)

    element = capfd.readouterr()

    assert "Détail complet du contrat 1 de l'entreprise Total" in element.out 
    assert "SI = Signé / NS = Non" in element.out 

def test_logclients(capfd, mock_user, mock_companys):
    clientcontract = ClientView()

    with patch('builtins.input', return_value='RET'):
        clientcontract.logclients(mock_user, mock_companys)

    element = capfd.readouterr()

    assert "Entreprises" in element.out 
    assert "Suprimer définitivement l'entreprise" in element.out 

def test_totalViewCompagny(capfd, mock_user, mock_company, mock_contacts):
    clientcontract = ClientView()

    with patch('builtins.input', return_value='RET'):
        clientcontract.totalViewCompagny(mock_user, mock_company, mock_contacts)

    element = capfd.readouterr()

    assert "Détail complet de l'entreprise Total" in element.out 
    assert "Créer un nouveau contact" in element.out 

def test_detailedContact(capfd, mock_user, mock_company, mock_contact):
    clientcontract = ClientView()

    with patch('builtins.input', return_value='RET'):
        clientcontract.detailedContact(mock_contact, mock_company)

    element = capfd.readouterr()

    assert "Information" in element.out 
    assert "Choix d'actions" in element.out 


def test_LiteViewCompagny(capfd, mock_user, mock_company, mock_contacts):
    clientcontract = ClientView()

    with patch('builtins.input', return_value='RET'):
        clientcontract.LiteViewCompagny(mock_user, mock_company, mock_contacts)

    element = capfd.readouterr()

    assert "Adresse de l'entreprise" in element.out 
    assert "Récapitulatif de l'entreprise Total" in element.out 


