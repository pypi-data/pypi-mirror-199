import pytest
from django.test import RequestFactory

from wcd_jwt.views import token_obtain_view, token_refresh_view
from django.views.decorators.csrf import csrf_exempt


obtain_view = csrf_exempt(token_obtain_view)
refresh_view = csrf_exempt(token_refresh_view)


@pytest.mark.django_db
def test_obtain(make_user, rf: RequestFactory):
    user, pswd = make_user('user')
    r = rf.post('/', {'username': user.username, 'password': pswd})

    response = obtain_view(r)

    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_refresh(make_user, rf: RequestFactory, monkeypatch, django_assert_num_queries):
    user, pswd = make_user('user')
    obtained = obtain_view(
        rf.post('/', {'username': user.username, 'password': pswd})
    )
    refreshed = refresh_view(
        rf.post('/', {'refresh': obtained.data['refresh']})
    )

    assert 'access' in refreshed.data
    assert 'refresh' not in refreshed.data

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)
        m.setattr('wcd_jwt.contrib.registry.conf.settings.TOKEN_REGISTRATION_PIPELINE', [
            'wcd_jwt.contrib.registry.services.pipeline.register_pairs',
            'wcd_jwt.contrib.registry.services.pipeline.connecting_user',
        ])

        # TODO: There is too much queries happening here.
        # Should rework it somehow.
        with django_assert_num_queries(9):
            refreshed2 = refresh_view(
                rf.post('/', {'refresh': obtained.data['refresh']})
            )

        assert 'access' in refreshed2.data
        assert 'refresh' in refreshed2.data
        assert refreshed2.data['refresh'] != obtained.data['refresh']

    with monkeypatch.context() as m:
        m.setattr('wcd_jwt.conf.settings.ROTATE_REFRESH_TOKENS', True)

        # TODO: There is too much queries happening here.
        # Should rework it somehow.
        with django_assert_num_queries(16):
            refreshed3 = refresh_view(
                rf.post('/', {'refresh': refreshed2.data['refresh']})
            )
