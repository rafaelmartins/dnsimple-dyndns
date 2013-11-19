# -*- coding: utf-8 -*-
"""
    dnsimple_dyndns.external_ip
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by Rafael Goncalves Martins
    :license: BSD, see LICENSE for more details.
"""

import requests


def get_external_ip():
    """Returns the current external IP, based on http://icanhazip.com/. It will
    probably fail if the network setup is too complicated or the service is
    down.
    """
    response = requests.get('http://icanhazip.com/')
    if not response.ok:
        raise RuntimeError('Failed to get external ip: %s' % response.content)
    return response.content.strip()
