# -*- coding: utf-8 -*-
"""
    dnsimple_dyndns.dnsimple
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by Rafael Goncalves Martins
    :license: BSD, see LICENSE for more details.
"""

import json
import requests


class DNSimple(object):

    def __init__(self, domain, domain_token):
        self._domain = domain
        self._baseurl = 'https://dnsimple.com/domains/%s/records' % \
            self._domain
        self._session = requests.Session()
        self._session.headers['X-DNSimple-Domain-Token'] = domain_token
        self._session.headers['Accept'] = 'application/json'

    def _format_hostname(self, name):
        if not len(name):
            return self._domain
        return '%s.%s' % (name, self._domain)

    def _get_record(self, name):
        """Returns the id of a record, if it exists."""
        request = self._session.get(self._baseurl, params={'name': name,
                                                           'type': 'A'})
        if not request.ok:
            raise RuntimeError('Failed to search record: %s - %s' %
                               (self._format_hostname(name), request.json()))
        records = request.json()
        if len(records) == 0:
            return
        record = records[0]
        if 'record' not in record or 'id' not in record['record']:
            raise RuntimeError('Invalid record JSON format: %s - %s' %
                               (self._format_hostname(name), request.json()))
        return int(record['record']['id'])

    def _create_record(self, name, address, ttl):
        """Creates a new record."""
        data = json.dumps({'record': {'name': name,
                                      'record_type': 'A',
                                      'content': address,
                                      'ttl': ttl}})
        headers = {'Content-Type': 'application/json'}
        request = self._session.post(self._baseurl, data=data, headers=headers)
        if not request.ok:
            raise RuntimeError('Failed to create new record: %s - %s' %
                               (self._format_hostname(name), request.json()))
        record = request.json()
        if 'record' not in record or 'id' not in record['record']:
            raise RuntimeError('Invalid record JSON format: %s - %s' %
                               (self._format_hostname(name), request.json()))
        return record['record']

    def _update_record(self, record_id, name, address, ttl):
        """Updates an existing record."""
        data = json.dumps({'record': {'name': name,
                                      'content': address,
                                      'ttl': ttl}})
        headers = {'Content-Type': 'application/json'}
        request = self._session.put(self._baseurl + '/%d' % record_id,
                                    data=data, headers=headers)
        if not request.ok:
            raise RuntimeError('Failed to update record: %s - %s' %
                               (self._format_hostname(name), request.json()))
        record = request.json()
        if 'record' not in record or 'id' not in record['record']:
            raise RuntimeError('Invalid record JSON format: %s - %s' %
                               (self._format_hostname(name), request.json()))
        return record['record']

    def update_record(self, name, address, ttl=60):
        """Updates a record, creating it if not exists."""
        record_id = self._get_record(name)
        if record_id is None:
            return self._create_record(name, address, ttl)
        return self._update_record(record_id, name, address, ttl)
