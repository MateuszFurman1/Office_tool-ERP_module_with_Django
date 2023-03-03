from datetime import date
from datetime import datetime
import pytest
from django.contrib.auth.models import Permission
from office_tool_app.models import User, Vacation, Delegation, MedicalLeave, Group
from django.test import Client
from django.urls import reverse
from django.shortcuts import redirect


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
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'pesel': '12345678901',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        're_password': 'testpassword',
        'birth_date': date(1990, 1, 1),
        'father_name': 'John',
        'mother_name': 'Doe',
        'family_name': 'Doe',
        'group': "",
        'position': 'Test Position',
    }
    client = Client()
    url = reverse('registration')
    response = client.post(url, data)
    print(response.content)
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert User.objects.filter(username='testuser').exists()


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
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'pesel': '12345678901',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        're_password': 'testpassword',
        'birth_date': date(1990, 1, 1),
        'father_name': 'John',
        'mother_name': 'Doe',
        'family_name': 'Doe',
        'group': "",
        'position': 'Test Position',
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


@pytest.mark.django_db
def test_createVacation_post_view(users):
    today = str(datetime.now().date())
    data = {
        'replacement': users[1].id,
        'vacation_from': today,
        'vacation_to': today
    }
    client = Client()
    url = reverse('create-vacation')
    client.force_login(users[0])
    response = client.post(url, data)
    assert 302 == response.status_code
    vacation = Vacation.objects.get(employee=users[0])
    assert vacation.replacement == users[1]
    assert str(vacation.vacation_from) == today
    assert str(vacation.vacation_to) == today


@pytest.mark.django_db
def test_vacationAccept_view(user_with_permission, vacations):
    client = Client()
    url = reverse('accept-vacation', args=(vacations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    assert 200 == response.status_code
    assert response.context['vacation'] == vacations[0]


# @pytest.mark.django_db
# def test_vacationAccept_post_view(user_with_permission, vacation):
#     client = Client()
#     url = reverse('accept-vacation', args=(vacation.pk, ))
#     client.force_login(user_with_permission)
#     response = client.post(url)
#     assert response.status_code == 302
#     vacation.refresh_from_db()
#     assert vacation.status == 'accepted'
@pytest.mark.django_db
def test_vacationAccept_post_view(user_with_permission, vacations):
    client = Client()
    url = reverse('accept-vacation', args=(vacations[0].pk, ))
    client.force_login(user_with_permission)
    response = client.post(url)
    assert user_with_permission.has_perm('office_tool_app.can_manage_employees')
    assert 302 == response.status_code


@pytest.mark.django_db
def test_vacationReject_view(user_with_permission, vacations):
    client = Client()
    vacation = vacations[0]
    vacation.status = 'pending'
    vacation.save()
    url = reverse('accept-vacation', args=(vacation.pk,))
    client.force_login(user_with_permission)
    response = client.post(url)
    vacation.refresh_from_db()
    assert vacation.status == 'accepted'
    assert response.status_code == 302
    assert response.url == reverse('manage-detail', args=(vacation.employee.username,))
    # client = Client()
    # url = reverse('accept-vacation', args=(vacations[0].pk, ))
    # client.force_login(user_with_permission)
    # response = client.post(url)
    # vacation = Vacation.objects.get(pk=vacations[0].pk)
    # assert vacation.status == 'accepted'
    # assert redirect('manage-detail', vacations[0].employee.username) == response.redirect_chain[0][0]
    
    
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