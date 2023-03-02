from datetime import datetime
import pytest
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from office_tool_app.models import Delegation, Vacation, MedicalLeave, \
    AddressHome, AddressCore, User, Group, Messages

@pytest.fixture
def users():
    name_lst = ['Arkadiusz', 'Marek', 'Janusz', 'Franciszek', 'Julius', 'Adrian']
    lst = []
    for user in range(6):
        lst.append(User.objects.create(username=name_lst[user - 1]))
    return lst


@pytest.fixture
def user():
    return User.objects.create(username='Tadeusz')


@pytest.fixture
def my_permission():
    permission, _ = Permission.objects.get_or_create(
        codename='can_manage_employees',
        name='can manage employees',
        content_type=ContentType.objects.get_for_model(User)
    )
    return permission


@pytest.fixture
def user_with_permission(my_permission):
    u = User.objects.create_user(
        username='Dariusz',
        email='testuser@example.com',
        password='password'
    )
    u.user_permissions.add(my_permission)
    return u
    # u = User.objects.create_user(
    #     username='Dariusz', 
    #     email='Dariusz@example.com', 
    #     password='123456'
    # )
    # user_ct = ContentType.objects.get(app_label='auth', model='user')
    # permission, created = Permission.objects.get_or_create(
    #     content_type=user_ct, 
    #     codename='can_manage_employees', 
    #     name="can manage employees"
    # )
    # # permission = Permission.objects.get(codename='can_manage_employees' )
    # # print(permission)
    # u.user_permissions.add(permission)
    # u.refresh_from_db()
    # return u


@pytest.fixture
def delegations(users):
    today = str(datetime.now().date())
    lst = []
    for n in range(5):
        p = Delegation.objects.create(employee=users[0], start_date=today, end_date=today, delegation_country='DE',
                                      status='pending')
        lst.append(p)
    return lst


@pytest.fixture
def vacation(users):
    today = str(datetime.now().date())
    vacation = Vacation.objects.create(
    employee=users[0],
    replacement=users[1],
    vacation_from=today,
    vacation_to=today,
    status='pending'
    )
    return vacation
    today = str(datetime.now().date())
    lst = []
    for n in range(5):
        p = Vacation.objects.create(employee=users[0], replacement=users[n + 1], vacation_from=today, vacation_to=today,
                                    status='pending')
        lst.append(p)
    return lst


@pytest.fixture
def medical_leaves(users):
    today = str(datetime.now().date())
    lst = []
    for n in range(5):
        p = MedicalLeave.objects.create(employee=users[0], from_date=today, to_date=today)
        lst.append(p)
    return lst


@pytest.fixture
def message(users):
    today = str(datetime.now().date())
    lst = []
    for n in range(5):
        p = Messages.objects.create(from_employee=users[n + 1], to_employee=users[0],
                                    sending_date=today, message='test')
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
    return lst