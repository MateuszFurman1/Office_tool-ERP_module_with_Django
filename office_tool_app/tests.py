from datetime import date
from datetime import datetime
import pytest
from office_tool_app.models import User, Vacation, Delegation, MedicalLeave
from django.test import Client
from django.urls import reverse

from office_tool_app.form import RegistrationForm, LoginForm, \
    AddressHomeForm, AddressCoreForm, UserUpdateForm, VacationForm, \
    DelegationForm, MedicalLeaveForm


@pytest.mark.django_db
def test_Home_view(user, vacations):
    client = Client()
    client.force_login(user)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration_get_view():
    client = Client()
    url = reverse('registration')
    response = client.get(url)
    assert 200 == response.status_code
    assert isinstance(response.context['form'], RegistrationForm)


@pytest.mark.django_db
def test_registration_post_valid_view():
    data = {
        'username': 'name1',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@email.com',
        'pesel': '2147483647',
        'birth_date': '2022-11-28',
        'father_name': 'test',
        'mother_name': 'test',
        'family_name': 'test',
        'group': '',
        'position': 'test',
        'password': '123',
        're_password': '123'
    }
    client = Client()
    url = reverse('registration')
    response = client.post(url, data)
    assert 302 == response.status_code
    assert User.objects.get(username='name1')


@pytest.mark.django_db
def test_registration_post_invalid_view():
    data = {
        'username': 'name1',
        'password': 'asd',
        're_password': '111'
    }
    client = Client()
    url = reverse('registration')
    response = client.post(url, data)
    assert 200 == response.status_code
    assert len(User.objects.all()) == 0
    assert isinstance(response.context['form'], RegistrationForm)


@pytest.mark.django_db
def test_login_get_view():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert 200 == response.status_code
    assert isinstance(response.context['form'], LoginForm)


@pytest.mark.django_db
def test_login_post_view_invalid_with_log():
    client = Client()
    url = reverse('login')
    data = {
        'username': 'test',
        'password': 'test',
        're_password': '123'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert isinstance(response.context['form'], LoginForm)
    assert len(User.objects.all()) == 0


@pytest.mark.django_db
def test_logout_get_view(user):
    client = Client()
    url = reverse('logout')
    client.force_login(user)
    response = client.get(url)
    assert 302 == response.status_code


@pytest.mark.django_db
def test_profile_get(user):
    client = Client()
    url = reverse('profile')
    client.force_login(user)
    response = client.get(url)
    assert 200 == response.status_code
    assert isinstance(response.context['form'], UserUpdateForm)


@pytest.mark.django_db
def test_profile_post(user):
    data = {
        'username': 'name1',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@email.com',
        'pesel': '2147483647',
        'birth_date': '2022-11-28',
        'father_name': 'test',
        'mother_name': 'test',
        'family_name': 'test',
        'group': '',
        'position': 'test',
    }
    client = Client()
    url = reverse('profile')
    client.force_login(user)
    response = client.post(url, data)
    assert 302 == response.status_code
    assert len(User.objects.all()) != 0


@pytest.mark.django_db
def test_vacationDetail_view(users, vacations):
    client = Client()
    url = reverse('vacation-detail')
    client.force_login(users[0])
    response = client.get(url)
    vacation_context = response.context['vacations_today']
    assert vacation_context.count() == len(vacations)
    for m in vacations:
        assert m in vacation_context


@pytest.mark.django_db
def test_createVacation_view(user):
    client = Client()
    url = reverse('create-vacation')
    client.force_login(user)
    response = client.get(url)
    assert 200 == response.status_code
    form = response.context['form']
    assert isinstance(form, VacationForm)

#Do poprawy !!!!
@pytest.mark.django_db
def test_createVacation_post_view(users):
    today = str(datetime.now().date())
    data = {
        'replacement': users[1],
        'vacation_from': today,
        'vacation_to': today
    }
    client = Client()
    url = reverse('create-vacation')
    client.force_login(users[0])
    response = client.post(url, data)
    assert 302 == response.status_code
    assert Vacation.objects.get(employee=users[0])

#Błąd!!! permision
@pytest.mark.django_db
def test_vacationAccept_view(user_with_permission, vacations):
    client = Client()
    url = reverse('accept-vacation', args=(vacations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    vacation_context = response.context['vacation']
    print(vacation_context)
    assert 200 == response.status_code
    assert vacation_context == vacations[0]


@pytest.mark.django_db
def test_vacationAccept_post_view(user_with_permission, vacations):
    client = Client()
    url = reverse('accept-vacation', args=(vacations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.post(url)
    assert 200 == response.status_code

#Błąd!!! persmision
@pytest.mark.django_db
def test_vacationReject_view(user_with_permission, vacations):
    client = Client()
    url = reverse('reject-vacation', args=(vacations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    vacation_context = response.context['vacation']
    print(vacation_context)
    assert 200 == response.status_code
    assert vacation_context == vacations[0]

#Błąd!!! persmision
@pytest.mark.django_db
def test_vacationReject_post_view(user_with_permission, vacations):
    client = Client()
    url = reverse('reject-vacation', args=(vacations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.post(url)
    assert 200 == response.status_code


@pytest.mark.django_db
def test_delegationDetail_view(users, delegations):
    client = Client()
    url = reverse('delegation-detail')
    client.force_login(users[0])
    response = client.get(url)
    delegation_context = response.context['delegations_today']
    assert delegation_context.count() == len(delegations)
    for m in delegations:
        assert m in delegation_context


@pytest.mark.django_db
def test_createDelegation_view(user):
    client = Client()
    url = reverse('create-delegation')
    client.force_login(user)
    response = client.get(url)
    assert 200 == response.status_code
    form = response.context['form']
    assert isinstance(form, DelegationForm)


@pytest.mark.django_db
def test_createDelegation_post_view(users):
    today = str(datetime.now().date())
    data = {
        'start_date': today,
        'end_date': today,
        'delegation_country': 'DE',
    }
    client = Client()
    url = reverse('create-delegation')
    client.force_login(users[0])
    response = client.post(url, data)
    assert 302 == response.status_code
    assert Delegation.objects.get(employee=users[0])


#Błąd!!! permision
@pytest.mark.django_db
def test_vacationAccept_view(user_with_permission, delegations):
    client = Client()
    url = reverse('accept-delegation', args=(delegations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    delegation_context = response.context['vacation']
    assert 200 == response.status_code
    assert delegation_context == delegations[0]


@pytest.mark.django_db
def test_delegationAccept_post_view(user_with_permission, delegations):
    client = Client()
    url = reverse('accept-delegation', args=(delegations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.post(url)
    assert 200 == response.status_code

#Błąd!!! persmision
@pytest.mark.django_db
def test_delegationReject_view(user_with_permission, delegations):
    client = Client()
    url = reverse('reject-delegation', args=(delegations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    delegation_context = response.context['delegation']
    assert 200 == response.status_code
    assert delegation_context == delegations[0]

#Błąd!!! persmision
@pytest.mark.django_db
def test_delegationnReject_post_view(user_with_permission, delegations):
    client = Client()
    url = reverse('reject-delegation', args=(delegations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.post(url)
    assert 200 == response.status_code


@pytest.mark.django_db
def test_medicalLeave_view(users, medical_leaves):
    client = Client()
    url = reverse('medical-leave')
    client.force_login(users[0])
    response = client.get(url)
    medical_context = response.context['medicals']
    assert medical_context.count() == len(medical_leaves)
    for m in medical_leaves:
        assert m in medical_context

#Błąd!!!! permision
@pytest.mark.django_db
def test_createMedicalLeave_view(user_with_permission):
    client = Client()
    url = reverse('create-medical', args=(user_with_permission.username, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    assert 200 == response.status_code
    form = response.context['form']
    assert isinstance(form, MedicalLeaveForm)

#Błąd!!!! permision
@pytest.mark.django_db
def test_createMedicalLeave_post_view(user_with_permission):
    today = str(datetime.now().date())
    data = {
        'from_date': today,
        'to_date': today,
    }
    client = Client()
    url = reverse('create-medical', args=(user_with_permission.username, ))
    client.force_login(user_with_permission)
    response = client.post(url, data)
    assert 302 == response.status_code
    assert MedicalLeave.objects.get(employee=user_with_permission)


@pytest.mark.django_db
def test_medicalLeave_delete_view(users, medical_leaves):
    client = Client()
    url = reverse('delete-medical', args=(medical_leaves[0].pk, ))
    client.force_login(users[0])
    response = client.get(url)
    medical_context = response.context['medical_leave']
    print(medical_context)
    assert 200 == response.status_code
    assert medical_leaves[0] == medical_context


@pytest.mark.django_db
def test_medicalLeave_delete_post_view(users, medical_leaves):
    client = Client()
    url = reverse('delete-medical', args=(medical_leaves[0].pk, ))
    client.force_login(users[0])
    response = client.post(url)
    assert 302 == response.status_code


@pytest.mark.django_db
def test_messages_view(users, message):
    client = Client()
    url = reverse('messages')
    client.force_login(users[0])
    response = client.get(url)
    messages_context = response.context['messages']
    print(messages_context)
    assert 200 == response.status_code
    assert len(message) == messages_context.count()

#Błąd!!! permision
@pytest.mark.django_db
def test_Manage_view(user_with_permission):
    client = Client()
    url = reverse('manage')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert 200 == response.status_code

#Błąd!!! permision
@pytest.mark.django_db
def test_ManageDetail_view(user_with_permission):
    client = Client()
    url = reverse('manage-detail', args=(user_with_permission.pk, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    assert 200 == response.status_code