from datetime import datetime
import pytest
from office_tool_app.models import Delegation, Vacation, MedicalLeave, AddressHome, AddressCore, User, Group


@pytest.fixture
def users():
    name_lst = ['Tadeusz', 'Marek', 'Janusz', 'Franciszek', 'Julius']
    lst = []
    for n in range(5):
        p = User.objects.create(username=name_lst[n-1])
        lst.append(p)
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
        p = Vacation.objects.create(employee=users[n-1], replacement=users[-1], vacation_from=n, vacation_to=today,
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
def address_home(users):
    lst = []
    for n in range(5):
        p = AddressHome.objects.create(employee=users[n-1], city=n, province=n, country_region=n, postal_code=n)
        lst.append(p)
    return lst


@pytest.fixture
def address_core(users):
    lst = []
    for n in range(5):
        p = AddressCore.objects.create(employee=users[n-1], city=n, province=n, country_region=n, postal_code=n)
        lst.append(p)
    return lst


@pytest.fixture
def groups(users):
    lst = []
    m = Group.objects.create(name='manager')
    e = Group.objects.create(name='employee')
    lst.append(m)
    lst.append(e)
    return  lst