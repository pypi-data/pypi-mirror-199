import pytest
from django.test import RequestFactory
from django.views.decorators.csrf import csrf_exempt

from wcd_jwt.views import token_obtain_view, token_refresh_view
from wcd_jwt.contrib.device_registry.models import TokenInterlocutorConnection
from wcd_device_recognizer.models import Interlocutor


obtain_view = csrf_exempt(token_obtain_view)
refresh_view = csrf_exempt(token_refresh_view)


@pytest.mark.django_db
def test_register_interlocutor(make_user, rf: RequestFactory):
    user, pswd = make_user('user')
    r = rf.post('/', {'username': user.username, 'password': pswd})
    response = obtain_view(r)

    assert 2 == TokenInterlocutorConnection.objects.count()
    assert 1 == Interlocutor.objects.count()
