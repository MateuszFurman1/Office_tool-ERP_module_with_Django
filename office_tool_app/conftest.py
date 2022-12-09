import pytest
from django.contrib.auth.models import User, Permission

from booking_rooms_app.models import Room, Comment


@pytest.fixture
def rooms():
    lst = []
    for n in range(10):
        p = Room.objects.create(name=n, seats=n, projector=False, created='2022-11-07 20:20:46.816306+01',
                                updated='2022-11-07 20:20:46.816306+01')
        lst.append(p)
    return lst


@pytest.fixture
def user():
    return User.objects.create(username='tadeusz')


@pytest.fixture
def comments(user):
    lst = []
    for n in range(5):
        p = Comment.objects.create(text=n, author=user)
        lst.append(p)
    return lst


