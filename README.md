dnsimple-dyndns
===============

Dynamic DNS implementation, that relies on DNSimple.com

This is a simple script that updates (and creates, if needed) an ``A`` domain record for any
``DNSimple.com`` managed domain. It is designed to be run as a hook script right after the
WAN connection.


Usage
-----

```
usage: dnsimple-dyndns [-h] [-v] [-t TTL] [-i IP]
                       DOMAIN DOMAIN-TOKEN RECORD-NAME

Dynamic DNS implementation, that relies on DNSimple.com.

positional arguments:
  DOMAIN             domain controlled by DNSimple.com
  DOMAIN-TOKEN       DNSimple.com domain API key.
  RECORD-NAME        name of the record to be updated.

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit
  -t TTL, --ttl TTL  DNS record TTL, defaults to 60
  -i IP, --ip IP     IP address, defaults to current external address from
                     http://icanhazip.com/
```


Running on Gentoo with OpenRC
-----------------------------

To run this script on Gentoo with OpenRC, you should emerge the ``dnsimple-dyndns`` package:

```
# emerge -av dnsimple-dyndns
```

Then add the following function to your ``/etc/conf.d/net`` file (or edit your postup function,
if already exists):

```bash
postup() {
    if [[ "${IFACE}" = "enp3s0" ]]; then
        einfo "Updated DNS record: $(dnsimple-dyndns example.com your-domain-token home)"
    else
        einfo "Ignoring interface: ${IFACE}"
    fi
}
```

Replace ``enp3s0`` with your WAN interface, ``example.com`` with your DNSimple.com managed domain,
``your-domain-token`` with your DNSimple.com domain token
(see http://developer.dnsimple.com/authentication/#dnsimple-domain-token) and ``home`` with your
desired DNS record name.


Running as a dhcpcd hook
------------------------

To run this script as a dhcpcd hook, you should add this content to your ``/etc/dhcpcd.exit-hook`` file:

```bash
if $if_up && [ "${interface}" = "enp3s0" ]; then
    syslog info "Updated DNS record: $(dnsimple-dyndns --ip "$new_ip_address" example.com your-domain-token home)"
fi
```

Replace ``enp3s0`` with your WAN interface, ``example.com`` with your DNSimple.com managed domain,
``your-domain-token`` with your DNSimple.com domain token
(see http://developer.dnsimple.com/authentication/#dnsimple-domain-token) and ``home`` with your
desired DNS record name.
