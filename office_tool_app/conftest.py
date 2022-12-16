from datetime import datetime
import pytest
from office_tool_app.models import Delegation, Vacation, MedicalLeave, AddressHome, AddressCore, User, Group


@pytest.fixture
def users():
    name_lst = ['Tadeusz', 'Marek', 'Janusz', 'Franciszek', 'Julius']
    lst = []
    lst.append(User.objects.create(username='Tadeusz'))
    lst.append(User.objects.create(username='Marek'))
    lst.append(User.objects.create(username='Janusz'))
    lst.append(User.objects.create(username='Franciszek'))
    lst.append(User.objects.create(username='Julius'))
    lst.append(User.objects.create(username='Julka'))
    lst.append(User.objects.create(username='Adrian'))
    return lst


@pytest.fixture
def user():
    return User.objects.create(username='Tadeusz')


@pytest.fixture
def delegations(users):
    today = str(datetime.now().date())
    lst = []
    for n in range(5):
        p = Delegation.objects.create(employee=users[n-1], start_date=n, end_date=today, delegation_country='DE',
                                      status='pending')
        lst.append(p)
    return lst


@pytest.fixture
def vacations(users):
    today = str(datetime.now().date())
    lst = []
    for n in range(5):
        p = Vacation.objects.create(employee=users[n], replacement=users[n+1], vacation_from=today, vacation_to=today,
                                    status='pending')
        lst.append(p)
    return lst


@pytest.fixture
def medical_leaves(users):
    today = str(datetime.now().date())
    lst = []
    for n in range(5):
        p = MedicalLeave.objects.create(employee=users[n-1], from_date=n, to_date=today)
        lst.append(p)
    return lst


@pytest.fixture
def address_home(user):
    return AddressHome.objects.create(employee=user, city='test', province='test', country_region='test',
                                      postal_code='test')


@pytest.fixture
def address_core(user):
    return AddressCore.objects.create(employee=user, city='test', province='test', country_region='test',
                                      postal_code='test')


@pytest.fixture
def groups(users):
    lst = []
    m = Group.objects.create(name='management')
    e = Group.objects.create(name='non-managerial employees')
    lst.append(m)
    lst.append(e)
    return  lst