import pytest
import time
from django.test import RequestFactory
from django.views.decorators.csrf import csrf_exempt

from wcd_jwt.views import token_obtain_view, token_refresh_view
from wcd_jwt.contrib.registry.models import Token


obtain_view = csrf_exempt(token_obtain_view)
refresh_view = csrf_exempt(token_refresh_view)


@pytest.mark.django_db
def test_obtain_tokens_registered(make_user, rf: RequestFactory):
    user, pswd = make_user('user')
    r = rf.post('/', {'username': user.username, 'password': pswd})
    response = obtain_view(r)

    assert 2 == Token.objects.filter(token__in=[
        response.data['refresh'], response.data['access']
    ]).count()


@pytest.mark.django_db
def test_refresh_tokens_registered(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    obtained = obtain_view(
        rf.post('/', {'username': user.username, 'password': pswd})
    ).data
    refreshed = refresh_view(
        rf.post('/', {'refresh': obtained['refresh']})
    ).data

    assert 'refresh' not in refreshed
    assert 1 == Token.objects.filter(token__in=[
        refreshed['access']
    ]).count()
    assert 3 == Token.objects.count()

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)
        refreshed2 = refresh_view(
            rf.post('/', {'refresh': obtained['refresh']})
        ).data

        assert 2 == Token.objects.filter(token__in=[
            refreshed2['refresh'], refreshed2['access']
        ]).count()
        assert 5 == Token.objects.count()

    parents = tuple(sorted([
        (obtained['refresh'], None),
        (obtained['access'], obtained['refresh']),
        (refreshed['access'], obtained['refresh']),
        (refreshed2['access'], refreshed2['refresh']),
        (refreshed2['refresh'], obtained['refresh']),
    ]))

    result = tuple(sorted(Token.objects.values_list('token', 'parent__token')))

    assert parents == result


@pytest.mark.django_db
def test_register_parallel(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    r = rf.post('/', {'username': user.username, 'password': pswd})
    run = {'yes': False}

    class RT:
        def __init__(self, target, args, kwargs, **kw):
            self.target = target
            self.args = args
            self.kwargs = kwargs

        def start(self):
            run['yes'] = True
            self.target(*self.args, **self.kwargs)

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.contrib.registry.utils.threading.Thread', RT)
        response = obtain_view(r)
        assert not run['yes']

        m.setattr('wcd_jwt.contrib.registry.conf.settings.TOKEN_REGISTRATION_ON_SIGNAL_PARALLEL', True)
        response = obtain_view(r)
        assert run['yes']

    assert 4 == Token.objects.count()


@pytest.mark.django_db
def test_disabled_autoregister(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    r = rf.post('/', {'username': user.username, 'password': pswd})

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.contrib.registry.conf.settings.TOKEN_REGISTRATION_ON_SIGNAL', False)
        response = obtain_view(r)
        refreshed = refresh_view(
            rf.post('/', {'refresh': response.data['refresh']})
        ).data

    assert 0 == Token.objects.count()
