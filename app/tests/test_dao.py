import pytest
from app.dao.userdao import UserDAO
from app.models.models import User
from datetime import datetime


# Constantes User
NOM = 'John Doe'
MAIL = 'jd@aa.fr'
MDP = 'fmt54TH51.BAR'
ROLE = 1

# Constantes Company
COMPANY_NAME = 'ENTREPRISE TEST'
COMPANY_ADRESS = '6 rue du perche 72300 sablé sur Sarthe'

# Constantes event
EVENT_DATE_START = datetime(2024, 8, 19, 10, 0, 0)
EVENT_DATE_END = datetime(2024, 8, 19, 12, 0, 0)
LOCATION = "TestAngers"
ATTENDEES = 50
NOTES = "Test notes"

# Constantes Contact
CONTACT_NAME = 'Marc BAR'
CONTACT_EMAIL = "mab@free.fr"
CONTACT_PHONE = "0123456789"
CONTACT_SIGNATORY = 1

# Constantes contracts
CONTRACT_TOTAL_AMONT = 181818.00
CONTRACT_CURRENT_AMONT = 1818.00
CONTRACT_SIGN = 1



@pytest.fixture(scope='function')
def dao():
    return UserDAO()

def test_tables(dao):
    dao.tables()
    tables = dao.metadata.tables.keys()
    assert 'user' in tables
    assert 'company' in tables
    assert 'client_contact' in tables
    assert 'contract' in tables
    assert 'event' in tables
    assert 'event_contract' in tables
    assert 'role' in tables
    assert 'texts' in tables

def test_get_all_users(dao):

    session = dao.Session()
    users = dao.get_all_users()
    assert len(users) >= 1

    session.close()

def test_creation_user(dao):
    session = dao.Session()
    dao.add_user(NOM, MAIL, MDP, ROLE)
    session.commit()
    user = dao.get_user_by_email(MAIL)
    assert user.nom == NOM
    assert user.email == MAIL

def test_multiple_get_user(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    user2 = dao.get_user(id)
    assert user.email == user2.email
    users = dao.get_user_by_role(1)
    assert any(user.email == MAIL for user in users)
    users2 = dao.get_all_users()
    assert any(user.email == MAIL for user in users2)
    users3 = dao.get_all_user_with_role_name()
    assert MAIL not in users3
    session.close()

def test_update_user(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    dao.update_user(id, 'Jane Doe', MAIL, ROLE)
    user3 = dao.get_user_by_email(MAIL)
    assert user3.nom == 'Jane Doe'
    dao.update_user(id, NOM, MAIL, ROLE)
    session.close()

def test_get_all_roles(dao):

    session = dao.Session()
    roles = dao.get_all_roles()
    assert len(roles) >= 1
    assert any(role.role == "Admin" for role in roles)
    assert any(role.role == "Support" for role in roles)
    assert any(role.role == "Sale" for role in roles)
    assert any(role.role == "Management" for role in roles)
    session.close()

def test_create_company(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    dao.add_company(COMPANY_NAME, id, COMPANY_ADRESS)
    session.commit()

def test_multiple_get_company(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys = dao.get_all_company()
    assert any(company.company_name == COMPANY_NAME for company in companys)
    companys2 = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys2 if company.address == COMPANY_ADRESS), None)
    assert any(company.address == COMPANY_ADRESS for company in companys2)
    company3 = dao.get_company(company_id)
    assert company3.company_name == COMPANY_NAME
    companys4 = dao.get_all_company_without_user()
    assert any(company.address != COMPANY_ADRESS for company in companys4)
    session.close()

def test_update_company(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys2 = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys2 if company.company_name == COMPANY_NAME), None)
    dao.update_company(company_id, COMPANY_NAME,'149 Avenue Patton', id)
    company3 = dao.get_company(company_id)
    assert company3.address == '149 Avenue Patton'
    session.close()

def test_add_event(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    event_id = dao.add_event(EVENT_DATE_START, EVENT_DATE_END, LOCATION, id, ATTENDEES, NOTES)
    event = dao.get_event(event_id)
    assert event.location == LOCATION
    assert event.attendees == ATTENDEES
    session.close()

def test_multiple_get_event(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    events = dao.get_all_events_by_user_id(id)
    assert any(event.location == LOCATION for event in events)
    events2 = dao.get_all_events()
    assert any(event.location == LOCATION for event in events2)
    events3  = dao.get_all_events_without_user()
    assert any(event.location != LOCATION for event in events3)
    session.close()

def test_update_event(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    events = dao.get_all_events_by_user_id(id)
    event_id = next((event.id for event in events if event.location == LOCATION), None)
    dao.update_event(event_id, EVENT_DATE_START, EVENT_DATE_END, LOCATION, id, 150, NOTES)
    event2 = dao.get_event(event_id)
    assert event2.attendees == 150
    session.close()

def test_add_get_contact(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys if company.company_name == COMPANY_NAME), None)
    dao.add_contact(company_id, CONTACT_NAME, CONTACT_EMAIL, CONTACT_PHONE, CONTACT_SIGNATORY)
    session.commit()
    contacts = dao.get_all_contact_by_company_id(company_id)
    contact_id = next((contact.id for contact in contacts if contact.name == CONTACT_NAME), None)
    contact = dao.get_contact(contact_id)
    assert contact.name == CONTACT_NAME
    assert contact.email == CONTACT_EMAIL
    session.close()

def test_multiple_get_contact(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys if company.company_name == COMPANY_NAME), None)
    contacts = dao.get_all_contact_by_company_id(company_id)
    assert any(contact.name == CONTACT_NAME for contact in contacts)
    contacts2 = dao.get_all_contact()
    assert any(contact.name == CONTACT_NAME for contact in contacts2)
    contacts3 = dao.get_all_contacts_by_user_id(id)
    assert any(contact.name == CONTACT_NAME for contact in contacts3)
    session.close()
    
def test_update_contact(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys if company.company_name == COMPANY_NAME), None)
    dao.add_contact(company_id, CONTACT_NAME, CONTACT_EMAIL, CONTACT_PHONE, CONTACT_SIGNATORY)
    contacts = dao.get_all_contact_by_company_id(company_id)
    contact_id = next((contact.id for contact in contacts if contact.name == CONTACT_NAME), None)
    dao.update_contact(contact_id, company_id, CONTACT_NAME, CONTACT_EMAIL, '12345678454', CONTACT_SIGNATORY)
    contact = dao.get_contact(contact_id)
    assert contact.phone == '12345678454'
    session.close()

def test_add_get_contract(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys if company.company_name == COMPANY_NAME), None)
    dao.add_contract(company_id, id,  CONTRACT_TOTAL_AMONT, CONTRACT_CURRENT_AMONT, CONTRACT_SIGN)
    session.commit()
    contracts = dao.get_all_my_contracts_sign(id)
    print(contracts)
    contract_id = next((contract.id for contract in contracts if contract.total_amont == CONTRACT_TOTAL_AMONT), None)
    print(contract_id)
    contract = dao.get_contract(contract_id)
    print(contract)
    assert contract.current_amont == CONTRACT_CURRENT_AMONT
    assert contract.total_amont == CONTRACT_TOTAL_AMONT
    session.close()

def test_multiple_get_contract(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys if company.company_name == COMPANY_NAME), None)
    contracts = dao.get_all_my_contracts_sign(id)
    assert any(contract.total_amont == CONTRACT_TOTAL_AMONT for contract in contracts)
    contracts2 = dao.get_all_contract()
    assert any(contract.total_amont == CONTRACT_TOTAL_AMONT for contract in contracts2)
    contracts3 = dao.get_all_contracts_by_company_id(company_id)
    assert any(contract.total_amont == CONTRACT_TOTAL_AMONT for contract in contracts3)
    contracts4 = dao.get_all_contracts_without_full_paiement(id)
    assert any(contract.total_amont == CONTRACT_TOTAL_AMONT for contract in contracts4)
    contracts5 = dao.get_all_contracts_by_user_id(id)
    assert any(contract.total_amont == CONTRACT_TOTAL_AMONT for contract in contracts5)
    contracts6 = dao.get_all_contracts_without_user()
    assert any(contract.total_amont != CONTRACT_TOTAL_AMONT for contract in contracts6)
    session.close()

def test_update_contract(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    contracts = dao.get_all_my_contracts_sign(id)
    contract_id = next((contract.id for contract in contracts if contract.total_amont == CONTRACT_TOTAL_AMONT), None)
    contract = dao.get_contract(contract_id)
    dao.update_contract(contract_id, contract.compagny_id, contract.user_id, contract.total_amont, 158.25, contract.sign)
    newcontract = dao.get_contract(contract_id)
    assert newcontract.current_amont == 158.25
    session.close()

def test_add_and_multiple_get_event_contract(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys if company.company_name == COMPANY_NAME), None)
    contracts = dao.get_all_my_contracts_sign(id)
    contract_id = next((contract.id for contract in contracts if contract.total_amont == CONTRACT_TOTAL_AMONT), None)
    events = dao.get_all_events_by_user_id(id)
    event_id = next((event.id for event in events if event.location == LOCATION), None)
    dao.add_event_contract(event_id,contract_id)
    contracts4 = dao.get_contract_for_event(event_id)
    assert any(contract.total_amont == CONTRACT_TOTAL_AMONT for contract in contracts4)
    events2 = dao.get_event_for_contract(contract_id)
    assert any(event.location == LOCATION for event in events2)
    events3 = dao.get_company_events(company_id)
    assert any(event.location == LOCATION for event in events3)
    dao.modify_event_contract(event_id, contract_id, contract_id)
    contracts5 = dao.get_contract_for_event(event_id)
    assert any(contract.total_amont == CONTRACT_TOTAL_AMONT for contract in contracts5)
    session.close()

def test_get_text(dao):
    session = dao.Session()
    text = dao.get_text(1)
    assert text is not None
    session.close()


########### test des deletes ############

def test_delete_event_contract(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    contracts = dao.get_all_my_contracts_sign(id)
    contract_id = next((contract.id for contract in contracts if contract.total_amont == CONTRACT_TOTAL_AMONT), None)
    events = dao.get_all_events_by_user_id(id)
    event_id = next((event.id for event in events if event.location == LOCATION), None)
    print(event_id, contract_id)
    dao.delete_event_contract(event_id, contract_id)
    deleted_events, deleted_contract = dao.get_event_contract(event_id,contract_id)
    assert deleted_events is None
    assert deleted_contract is None
    session.close()

def test_delete_contract(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    contracts = dao.get_all_my_contracts_sign(id)
    contract_id = next((contract.id for contract in contracts if contract.total_amont == CONTRACT_TOTAL_AMONT), None)
    dao.delete_contract(contract_id)
    deleted_contract = dao.get_contract(contract_id)
    assert deleted_contract is None
    session.close()

def test_delete_contact(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    companys2 = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys2 if company.address == COMPANY_ADRESS), None)
    dao.add_contact(company_id, CONTACT_NAME, CONTACT_EMAIL, CONTACT_PHONE, CONTACT_SIGNATORY)
    contacts = dao.get_all_contact_by_company_id(company_id)
    contact_id = next((contact.id for contact in contacts if contact.name == CONTACT_NAME), None)
    dao.delete_contact(contact_id)
    deleted_contact = dao.get_contact(contact_id)
    assert deleted_contact is None
    session.close()

def test_delete_event(dao):
    session = dao.Session()
    events = dao.get_all_events_by_user_id(id)
    event_id = next((event.id for event in events if event.location == LOCATION), None)
    dao.delete_event(event_id)
    deleted_event = dao.get_event(event_id)
    assert deleted_event is None, "test passé avec succès"
    session.close()

def test_delete_company(dao):
    session = dao.Session()
    companys = dao.get_company_by_user_id(id)
    company_id = next((company.id for company in companys if company.address == COMPANY_ADRESS), None)
    dao.delete_company(company_id)
    deleted_company = dao.get_company(company_id)
    assert deleted_company is None, "test passé avec succès"
    session.close()

def test_delete_user(dao):
    session = dao.Session()
    user = dao.get_user_by_email(MAIL)
    id = user.id
    dao.delete_user(id)
    deleted_user = dao.get_user(id)
    assert deleted_user is None, "test passé avec succès"
    session.close()