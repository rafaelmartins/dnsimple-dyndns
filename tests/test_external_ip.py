import mock
import pytest


def test_remote_ip():
    p = mock.patch('dnsimple_dyndns.external_ip.requests')
    with p as m:
        m.get.return_value = mock.Mock(content='127.0.0.1', ok=True)
        from dnsimple_dyndns.external_ip import get_external_ip
        ip = get_external_ip()
        assert ip == '127.0.0.1'
        m.get.assert_called_once_with('http://icanhazip.com/')


def test_remote_ip_error():
    p = mock.patch('dnsimple_dyndns.external_ip.requests')
    with p as m:
        m.get.return_value = mock.Mock(content='127.0.0.1', ok=False)
        from dnsimple_dyndns.external_ip import get_external_ip
        with pytest.raises(RuntimeError):
            get_external_ip()
