# -*- coding: utf-8 -*-
"""
    dnsimple_dyndns
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by Rafael Goncalves Martins
    :license: BSD, see LICENSE for more details.
"""

import argparse

from dnsimple_dyndns.dnsimple import DNSimple
from dnsimple_dyndns.external_ip import get_external_ip

__version__ = '0.1'


def main():
    parser = argparse.ArgumentParser(description='Dynamic DNS implementation, '
                                     'that relies on DNSimple.com.',
                                     version=__version__)
    parser.add_argument('-t', '--ttl', type=int, default=60,
                        help='DNS record TTL, defaults to 60')
    parser.add_argument('-i', '--ip', help='IP address, defaults to current '
                        'external address from http://icanhazip.com/')
    parser.add_argument('domain', metavar='DOMAIN',
                        help='domain controlled by DNSimple.com')
    parser.add_argument('domain_token', metavar='DOMAIN-TOKEN',
                        help='DNSimple.com domain API key.')
    parser.add_argument('record_name', metavar='RECORD-NAME',
                        help='name of the record to be updated.')

    args = parser.parse_args()
    dns = DNSimple(args.domain, args.domain_token)
    record = dns.update_record(args.record_name, args.ip or get_external_ip(),
                               args.ttl)
    print record['content']
    return 0
