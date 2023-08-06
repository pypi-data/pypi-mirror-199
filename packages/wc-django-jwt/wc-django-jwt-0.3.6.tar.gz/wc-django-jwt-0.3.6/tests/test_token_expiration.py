import pytest
from datetime import timedelta
from django.test import RequestFactory
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.utils import aware_utcnow

from wcd_jwt.views import token_obtain_view, token_refresh_view
from wcd_jwt.contrib.registry.models import Token
from wcd_jwt.contrib.registry.views import token_expire_view
from wcd_jwt.contrib.registry.services import token_manager, archiver


obtain_view = csrf_exempt(token_obtain_view)
refresh_view = csrf_exempt(token_refresh_view)
expire_view = csrf_exempt(token_expire_view)


@pytest.mark.django_db
def test_expire_part(make_user, rf: RequestFactory):
    user, pswd = make_user('user')
    r = rf.post('/', {'username': user.username, 'password': pswd})
    response = obtain_view(r).data

    assert 0 == Token.objects.expired().count()

    response2 = obtain_view(r).data

    token_manager.expire([AccessToken(response2['access'])], affect_tree=True)

    assert 2 == Token.objects.expired().count()
    assert 0 == (
        Token.objects
        .filter(token__in=[response['access'], response['refresh']])
        .expired().count()
    )


@pytest.mark.django_db
def test_expire_large_tree(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    obtained = obtain_view(
        rf.post('/', {'username': user.username, 'password': pswd})
    ).data
    refreshed = refresh_view(
        rf.post('/', {'refresh': obtained['refresh']})
    ).data

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)
        refresh_view(rf.post('/', {'refresh': obtained['refresh']}))

    assert 0 == Token.objects.expired().count()
    assert 5 == Token.objects.count()
    token_manager.expire([AccessToken(obtained['access'])])
    assert 1 == Token.objects.expired().count()
    token_manager.expire([AccessToken(refreshed['access'])], affect_tree=True)
    assert 5 == Token.objects.expired().count()


@pytest.mark.django_db
def test_expire_view(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    obtained = obtain_view(
        rf.post('/', {'username': user.username, 'password': pswd})
    ).data
    refreshed = refresh_view(
        rf.post('/', {'refresh': obtained['refresh']})
    ).data

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)
        refresh_view(rf.post('/', {'refresh': obtained['refresh']}))

    assert 0 == Token.objects.expired().count()
    assert 5 == Token.objects.count()
    expire_view(
        rf.post('/', {'token': obtained['access']})
    ).data
    assert 1 == Token.objects.expired().count()
    expire_view(
        rf.post('/', {'token': refreshed['access'], 'affect_tree': True})
    ).data
    assert 5 == Token.objects.expired().count()

    response = expire_view(
        rf.post('/', {'token': obtained['access']})
    )
    assert response.status_code == 400
    assert response.data['token'][0].code == 'token_expired'

    response = expire_view(
        rf.post('/', {'token': 'wrongkoken'})
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_expire_on_refresh(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    obtained = obtain_view(
        rf.post('/', {'username': user.username, 'password': pswd})
    ).data
    refreshed = refresh_view(
        rf.post('/', {'refresh': obtained['refresh']})
    ).data

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.contrib.registry.conf.settings.TOKEN_EXPIRE_ON_REFRESH', True)
        refresh_view(rf.post('/', {'refresh': obtained['refresh']}))

        assert 2 == Token.objects.expired().count()
        assert 2 == Token.objects.active().count()

        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)
        refresh_view(rf.post('/', {'refresh': obtained['refresh']}))

        assert 4 == Token.objects.expired().count()
        assert 2 == Token.objects.active().count()


@pytest.mark.django_db
def test_archiver(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    obtained = obtain_view(
        rf.post('/', {'username': user.username, 'password': pswd})
    ).data
    refreshed = refresh_view(
        rf.post('/', {'refresh': obtained['refresh']})
    ).data

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)
        refresh_view(rf.post('/', {'refresh': obtained['refresh']}))

    assert 0 == Token.objects.expired().count()
    assert 5 == Token.objects.count()

    expired = (
        Token.objects
        .filter(token__in=[obtained['refresh'], obtained['access']])
        .update(internal_expired_at=aware_utcnow() - timedelta(seconds=1))
    )

    assert 2 == Token.objects.expired().count()
    assert 5 == Token.objects.count()

    archiver.archive()

    assert 0 == Token.objects.expired().count()
    assert 3 == Token.objects.count()
