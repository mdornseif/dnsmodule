# $Id: dns.py,v 1.1 2001/07/09 21:10:51 drt Exp $
#
# Frondend to Bernsteins DNS Library

import _dns
import struct

def ip4tostr(ip):
    if len(ip) != 4:
        raise TypeError, 'ip must be exactly 4 bytes long'
    
    (a, b, c, d) = struct.unpack('BBBB', ip)
    return "%u.%u.%u.%u" % (a, b, c, d)

def ip4(fqdn):
    ip = _dns.ip4(fqdn)

    ret = []
    while len(ip):
        x = ip[:4]
        ip = ip[4:]
        ret.append(ip4tostr(x))

    return ret
