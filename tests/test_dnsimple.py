import mock
import pytest


@pytest.fixture
def patched_session(request):
    p = mock.patch('dnsimple_dyndns.dnsimple.requests.Session')

    def fin():
        p.stop()
    request.addfinalizer(fin)

    return p.start()


@pytest.fixture
def dnsimple():
    from dnsimple_dyndns.dnsimple import DNSimple
    return DNSimple('google.com', 'ok')


def test_format_host_name(dnsimple):
    assert 'test.google.com' == dnsimple._format_hostname('test')
    assert 'google.com' == dnsimple._format_hostname('')


def test_get_record(patched_session, dnsimple):
    response = mock.Mock(ok=True)
    response.json.return_value = [{'record': {'id': 1}}]
    patched_session().get.return_value = response

    assert 1 == dnsimple._get_record('ok')
    patched_session().get.assert_called_once_with(dnsimple._baseurl, params={
        'name': 'ok',
        'type': 'A'
    })


def test_get_record_without_return(patched_session, dnsimple):
    response = mock.Mock(ok=True)
    response.json.return_value = []
    patched_session().get.return_value = response

    assert None == dnsimple._get_record('ok')


def test_get_record_error(patched_session, dnsimple):
    response = mock.Mock(ok=False)
    response.json.return_value = 'any error'
    patched_session().get.return_value = response

    with pytest.raises(RuntimeError):
        dnsimple._get_record('ok')
