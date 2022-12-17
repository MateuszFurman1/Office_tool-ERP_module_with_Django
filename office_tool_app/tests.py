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
def test_Home_view(user):
    client = Client()
    client.force_login(user)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    # persons_context = response.context['rooms']
    # assert persons_context.count() == len(rooms)
    # for p in rooms:
    #     assert p in persons_context


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
    print(User.objects.all())
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

#Nie creationVacation post oraz nie zrobiłem
# dla vacation detail, vacation accept, vaccation reject
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

#Nie creationVacation post oraz nie zrobiłem
# dla vacation detail, vacation accept, vaccation reject
@pytest.mark.django_db
def test_createVacation_post_view(users):
    today = str(datetime.now().date())
    data = {
        'replacement': users[1],
        'vacation_from': today,
        'vacation_to': today,
        'user': users[0]
    }
    client = Client()
    url = reverse('create-vacation')
    client.force_login(users[0])
    response = client.post(url, data)
    assert 302 == response.status_code
    assert Vacation.objects.get(employee=users[0])


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

#Nie creationVacation post oraz nie zrobiłem
# dla vacation detail, vacation accept, vaccation reject
@pytest.mark.django_db
def test_createDelegation_post_view(users):
    today = str(datetime.now().date())
    data = {
        'start_date': today,
        'end_date': today,
        'delegation_country': 'DE',
        'user': users[0]
    }
    client = Client()
    url = reverse('create-delegation')
    client.force_login(users[0])
    response = client.post(url, data)
    assert 302 == response.status_code
    assert Delegation.objects.get(employee=users[0])


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


@pytest.mark.django_db
def test_createMedicalLeave_view(user_with_permission):
    client = Client()
    url = reverse('create-medical', args=(user_with_permission.username, ))
    client.force_login(user_with_permission)
    response = client.get(url)
    assert 200 == response.status_code
    form = response.context['form']
    assert isinstance(form, MedicalLeaveForm)

#Nie creationVacation post oraz nie zrobiłem
# dla vacation detail, vacation accept, vaccation reject
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
def test_medicalLeave_view(users, medical_leaves):
    client = Client()
    url = reverse('delete-medical', args=(medical_leaves[0].pk, ))
    client.force_login(users[0])
    response = client.get(url)
    medical_context = response.context['medical_leave']
    print(medical_context)
    assert 200 == response.status_code
    assert medical_leaves[0] == medical_context

# @pytest.mark.django_db
# def test_create_room_get_view(user):
#     client = Client()
#     url = reverse('create-room')
#     client.force_login(user)
#     response = client.get(url)
#     assert 200 == response.status_code
#     assert isinstance(response.context['form'], RoomForm)
#
#
# @pytest.mark.django_db
# def test_create_room_post_view_with_log(user):
#     client = Client()
#     url = reverse('create-room')
#     client.force_login(user)
#     data = {
#         'name': 'room',
#         'seats': 100,
#         'projector': False
#     }
#     response = client.post(url, data)
#     assert response.status_code == 302
#     assert Room.objects.get(name='room', seats=100, projector=False)
#
#
#
#
#
# @pytest.mark.django_db
# def test_edit_room_get_view_with_perm(user, rooms):
#     client = Client()
#     url = reverse('edit-room')
#     client.force_login(user)
#     room = rooms[0]
#     data = {
#         'id': room.id,
#         'name': 'room',
#         'seats': 100,
#         'projector': False
#     }
#     response = client.get(url, data)
#     assert 200 == response.status_code
#     assert isinstance(response.context['form'], RoomForm)
#
#
# @pytest.mark.django_db
# def test_edit_room_post_view_with_perm(user, rooms):
#     client = Client()
#     url = reverse('edit-room')
#     client.force_login(user)
#     room = rooms[0]
#     data = {
#         'id': room.id,
#         'name': 'room',
#         'seats': 100,
#         'projector': False
#     }
#     response = client.post(url, data)
#     assert response.status_code == 302
#     assert Room.objects.get(name='room', seats=100, projector=False)
#
#
# @pytest.mark.django_db
# def test_delete_room_get_view_with_perm(user, rooms):
#     client = Client()
#     url = reverse('delete-room')
#     client.force_login(user)
#     room = rooms[0]
#     data = {
#         'id': room.id,
#         'name': 'room',
#         'seats': 100,
#         'projector': False
#     }
#     response = client.get(url, data)
#     assert response.status_code == 302
#     assert len(Room.objects.all()) == 9  # przekazujemy 10 objektów i jeden usuwamy
#
#
# @pytest.mark.django_db
# def test_reservation_room_get_view_with_perm(user, rooms):
#     client = Client()
#     url = reverse('room-reserve')
#     client.force_login(user)
#     room = rooms[0]
#     data = {
#         'id': room.id,
#     }
#     response = client.get(url, data)
#     assert response.status_code == 200
#     assert isinstance(response.context['form'], ReservationForm)
#
#
# @pytest.mark.django_db
# def test_reservation_room_post_view_with_perm(user, rooms):
#     client = Client()
#     url = reverse('room-reserve')
#     client.force_login(user)
#     room = rooms[0]
#     data = {
#         'id': room.id,
#         'date': date.today(),
#         'comment': 'test'
#     }
#     response = client.post(url, data)
#     assert response.status_code == 302
#     assert Reservation.objects.get(room=room)
#
#
# @pytest.mark.django_db
# def test_reservation_room_post_view_invalid_with_perm(user, rooms):
#     client = Client()
#     url = reverse('room-reserve')
#     client.force_login(user)
#     room = rooms[0]
#     data = {
#         'id': room.id,
#         'room': room,
#         'date': '2022-11-07 20:20:46.816306+01',
#     }
#     response = client.post(url, data)
#     assert response.status_code == 200
#     assert len(Reservation.objects.all()) == 0
#     assert isinstance(response.context['form'], ReservationForm)
#
#
# @pytest.mark.django_db
# def test_detail_room_get_view(rooms):
#     client = Client()
#     url = reverse('detail-room')
#     room = rooms[0]
#     data = {
#         'id': room.id,
#     }
#     response = client.get(url, data)
#     assert 200 == response.status_code
#
#
# @pytest.mark.django_db
# def test_search_room_get_view(rooms):
#     client = Client()
#     url = reverse('search-room')
#     room = rooms[0]
#     data = {
#         'rooms':rooms,
#         'room-name': room.name,
#         'seats': room.seats
#     }
#     response = client.get(url, data)
#     assert 200 == response.status_code
#
#

#
#
# @pytest.mark.django_db
# def test_registration_get_view():
#     client = Client()
#     url = reverse('registration')
#     response = client.get(url)
#     assert 200 == response.status_code
#     assert isinstance(response.context['form'], RegistrationForm)
#
#
# @pytest.mark.django_db
# def test_registration_post_valid_view():
#     data = {
#         'username': 'name1',
#         'password': 'asd',
#         're_password': 'asd'
#     }
#     client = Client()
#     url = reverse('registration')
#     response = client.post(url, data)
#     assert 302 == response.status_code
#     assert User.objects.get(username='name1')
#
#
# @pytest.mark.django_db
# def test_registration_post_invalid_view():
#     data = {
#         'username': 'name1',
#         'password': 'asd',
#         're_password': '111'
#     }
#     client = Client()
#     url = reverse('registration')
#     response = client.post(url, data)
#     assert 200 == response.status_code
#     assert len(User.objects.all()) == 0
#     assert isinstance(response.context['form'], RegistrationForm)
#
#
# @pytest.mark.django_db
# def test_About_view(comments):
#     client = Client()
#     url = reverse('about')
#     response = client.get(url)
#     comment_context = response.context['comments']
#     assert 200 == response.status_code
#     assert comment_context.count() == len(comments)
#     for p in comments:
#         assert p in comment_context
#
#
# @pytest.mark.django_db
# def test_addcomment_room_post_view(user):
#     client = Client()
#     url = reverse('add-comment')
#     client.force_login(user)
#     data = {
#         'text': 'Test'
#     }
#     response = client.post(url, data)
#     assert 302 == response.status_code
#     assert Comment.objects.get(text='Test')
#
#
# @pytest.mark.django_db
# def test_profile_get_view(user):
#     client = Client()
#     url = reverse('profile', args=(user.username, ))
#     client.force_login(user)
#     response = client.get(url)
#     assert 200 == response.status_code
#     assert isinstance(response.context['form'], UserUpdateForm)
#
#
# @pytest.mark.django_db
# def test_profile_post_valid_view(user):
#     data = {
#         'first_name': 'test',
#         'last_name': 'test2',
#         'email': 'test@test.com',
#         'last_login': '2022-10-28 20:36:30.412291+02',
#         'date_joined': '2022-10-28 20:36:30.412291+02',
#     }
#     client = Client()
#     url = reverse('profile', args=(user.username, ))
#     client.force_login(user)
#     response = client.post(url, data)
#     assert 302 == response.status_code
#     assert len(User.objects.all()) != 0