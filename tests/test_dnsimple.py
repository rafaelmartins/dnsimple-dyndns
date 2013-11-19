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


def test_create_record(patched_session, dnsimple):
    response = mock.Mock(ok=True)
    response.json.return_value = {'record': {'id': 10, 'content': '127.0.0.1'}}

    patched_session().post.return_value = response
    assert {'id': 10, 'content': '127.0.0.1'} == dnsimple._create_record('ok', '127.0.0.1', 60)
    patched_session().post.assert_called_once_with(dnsimple._baseurl,
                                                   headers={'Content-Type': 'application/json'},
                                                   data='{"record": {"content": "127.0.0.1", "record_type": "A", "name": "ok", "ttl": 60}}')


def test_create_record_invalid_http_code(patched_session, dnsimple):
    response = mock.Mock(ok=False)
    response.json.return_value = 'anything'

    patched_session().post.return_value = response
    with pytest.raises(RuntimeError):
        dnsimple._create_record('ok', '127.0.0.1', 60)


def test_create_record_invalid_json_format(patched_session, dnsimple):
    response = mock.Mock(ok=True)
    response.json.return_value = {}

    patched_session().post.return_value = response
    with pytest.raises(RuntimeError):
        dnsimple._create_record('ok', '127.0.0.1', 60)


def test_update_record(patched_session, dnsimple):
    response = mock.Mock(ok=True)
    response.json.return_value = {'record': {'id': 10, 'content': '127.0.0.1'}}

    patched_session().put.return_value = response
    assert {'id': 10, 'content': '127.0.0.1'} == dnsimple._update_record(10, 'ok', '127.0.0.1', 60)
    patched_session().put.assert_called_once_with('%s/10' % dnsimple._baseurl,
                                                  headers={'Content-Type': 'application/json'},
                                                  data='{"record": {"content": "127.0.0.1", "name": "ok", "ttl": 60}}')


def test_update_record_invalid_http_code(patched_session, dnsimple):
    response = mock.Mock(ok=False)
    response.json.return_value = 'anything'

    patched_session().put.return_value = response
    with pytest.raises(RuntimeError):
        dnsimple._update_record(10, 'ok', '127.0.0.1', 60)


def test_update_record_invalid_json_format(patched_session, dnsimple):
    response = mock.Mock(ok=True)
    response.json.return_value = {}

    patched_session().put.return_value = response
    with pytest.raises(RuntimeError):
        dnsimple._update_record(10, 'ok', '127.0.0.1', 60)


def test_main_update_record_with_existing_record(patched_session, dnsimple):
    get_record = mock.Mock(ok=True)
    get_record.json.return_value = [{'record': {'id': 1}}]

    update_record = mock.Mock(ok=True)
    update_record.json.return_value = {'record': {'id': 10, 'content': '127.0.0.1'}}

    patched_session().get.return_value = get_record
    patched_session().put.return_value = update_record

    assert {'id': 10, 'content': '127.0.0.1'} == dnsimple.update_record('ok', '127.0.0.1', 60)


def test_main_update_record_with_non_existing_record(patched_session, dnsimple):
    get_record = mock.Mock(ok=True)
    get_record.json.return_value = []

    create_record = mock.Mock(ok=True)
    create_record.json.return_value = {'record': {'id': 10, 'content': '127.0.0.1'}}

    patched_session().get.return_value = get_record
    patched_session().post.return_value = create_record

    assert {'id': 10, 'content': '127.0.0.1'} == dnsimple.update_record('ok', '127.0.0.1', 60)
