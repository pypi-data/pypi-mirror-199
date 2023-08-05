import pytest
from django.test import RequestFactory
from django.views.decorators.csrf import csrf_exempt

from wcd_jwt.views import token_obtain_view, token_refresh_view
from wcd_jwt.contrib.registry.models import Token, TokenUserConnection


obtain_view = csrf_exempt(token_obtain_view)
refresh_view = csrf_exempt(token_refresh_view)


@pytest.mark.django_db
def test_refresh_tokens_registered(make_user, rf: RequestFactory, monkeypatch):
    user, pswd = make_user('user')
    obtained = obtain_view(
        rf.post('/', {'username': user.username, 'password': pswd})
    ).data
    refreshed = refresh_view(
        rf.post('/', {'refresh': obtained['refresh']})
    ).data

    assert 1 == TokenUserConnection.objects.filter(token__token__in=[
        refreshed['access']
    ]).count()
    assert 3 == TokenUserConnection.objects.count()
    assert 3 == TokenUserConnection.objects.filter(user=user).count()

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)
        refreshed2 = refresh_view(
            rf.post('/', {'refresh': obtained['refresh']})
        ).data

        assert 2 == TokenUserConnection.objects.filter(token__token__in=[
            refreshed2['refresh'], refreshed2['access']
        ]).count()
        assert 5 == TokenUserConnection.objects.count()
        assert 5 == TokenUserConnection.objects.filter(user=user).count()
