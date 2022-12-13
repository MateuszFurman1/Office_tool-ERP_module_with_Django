from datetime import date
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from office_tool_app.form import RegistrationForm


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
    client = Client()  # otwieramt przeglądarkę
    url = reverse('registration')  # mówimy na jaki url chcemy wejsc
    response = client.post(url, data)  # wchodzimu na url
    assert 200 == response.status_code
    assert len(User.objects.all()) == 0
    # albo funkcją count()
    assert isinstance(response.context['form'], RegistrationForm)


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
# @pytest.mark.django_db
# def test_login_get_view():
#     client = Client()
#     url = reverse('login')
#     response = client.get(url)
#     assert 200 == response.status_code
#     assert isinstance(response.context['form'], LoginForm)
#
#
# @pytest.mark.django_db
# def test_login_post_view_invalid_with_log():
#     client = Client()
#     url = reverse('login')
#     data = {
#         'username': 'test',
#         'password': 'test',
#         # 'captcha': True
#     }
#     response = client.post(url, data)
#     assert response.status_code == 200
#     assert isinstance(response.context['form'], LoginForm)
#     assert len(User.objects.all()) == 0
#
#
# @pytest.mark.django_db
# def test_logout_get_view(user):
#     client = Client()
#     url = reverse('logout')
#     client.force_login(user)
#     response = client.get(url)
#     assert 302 == response.status_code
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