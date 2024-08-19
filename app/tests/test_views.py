import pytest
from app.view.views import View
from app.view.userviews import UserView
from unittest.mock import Mock, patch
from app.dao.userdao import UserDAO


@pytest.fixture
def mock_user():
    user = Mock()
    user.email = "eric@gmail.com"
    user.nom = "Eric BARILLER"
    return user

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
    event1.event_date_start = Mock()
    event1.event_date_start.strftime = Mock(return_value="2024-08-19 10:00:00")

    event2 = Mock()
    event2.id = 2
    event2.attendees = 20
    event2.event_date_start = Mock()
    event2.event_date_start.strftime = Mock(return_value="2024-08-20 12:00:00")

    return [event1, event2]

@pytest.fixture
def mock_companys():
    company1 = Mock()
    company1.id = 1
    company1.company_name = "Company A"

    company2 = Mock()
    company2.id = 2
    company2.company_name = "Company B"

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

    captured = capfd.readouterr()

    assert "Liste des persones correpondantes" in captured.out
    assert "Utilisateurs" in captured.out

    for user in mock_users:
        assert str(user.id) in captured.out
        assert user.nom in captured.out
        assert user.email in captured.out


    assert "Attribuer l'évènement a <id>" in captured.out
    assert "Retour au menu précédent" in captured.out
    assert "Quitter le programme" in captured.out