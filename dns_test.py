# $Id: dns_test.py,v 1.1 2001/07/09 21:10:52 drt Exp $
import dns
import unittest

class general(unittest.TestCase):

    ip4tostrValues =  [('127.0.0.1', '\x7f\x00\x00\x01'),
                 ('0.0.0.0', '\x00\x00\x00\x00'),
                 ('1.1.1.1', '\x01\x01\x01\x01')]
    ip4Values =  [('', []),
                  ('127.0.0.1', ['127.0.0.1']),
                  ('[127.0.0.1]', ['127.0.0.1']),
                  ('127.0.0.1.127.0.0.1', ['127.0.0.1', '127.0.0.1']),
                  ('[127.0.0.1].[127.0.0.1]', ['127.0.0.1', '127.0.0.1']),
                  ('[127.0.0.1].127.0.0.1', ['127.0.0.1', '127.0.0.1']),
                  ('[127.0.0.1.127.0.0.1]', ['127.0.0.1', '127.0.0.1']),
                  ('[256.256.256.256]', ['0.0.0.0']),
                  ('[257.257.257.257]', ['1.1.1.1']),
                  ('[0.0.0.0]', ['0.0.0.0']),
                  ('[1.1.1.1]', ['1.1.1.1']),
                  ('dnstest.c0re.23.nu', ['1.2.3.45']),
                  #('multi.dnstest.c0re.23.nu', ['6.6.6.6', '5.5.5.5', '1.1.1.1', '8.8.8.8', '4.4.4.4', '3.3.3.3', '7.7.7.7', '2.2.2.2']),
                  ('none.dnstest.c0re.23.nu', []),
                  ('broken.dnstest.c0re.23.nu', []),
                  ('localhost', ['127.0.0.1']),
                  ('ftp.porn.org', ['127.0.0.1']),
                  ('www.example.com', ['128.9.176.32']),
                  ('a.root-servers.net', ['198.41.0.4']),
                  ('b.root-servers.net', ['128.9.0.107']),
                  ('c.root-servers.net', ['192.33.4.12']),
                  ('d.root-servers.net', ['128.8.10.90']),
                  ('e.root-servers.net', ['192.203.230.10']),
                  ('f.root-servers.net', ['192.5.5.241']),
                  ('g.root-servers.net', ['192.112.36.4']),
                  ('h.root-servers.net', ['128.63.2.53']),
                  ('i.root-servers.net', ['192.36.148.17']),
                  ('k.root-servers.net', ['193.0.14.129']),
                  ('l.root-servers.net', ['198.32.64.12']),
                  ('m.root-servers.net', ['202.12.27.33'])]

    def testip4tostr(self):
        for (str, ip)  in self.ip4tostrValues:
            result = dns.ip4tostr(ip)
            self.assertEqual(str, result)


    def testip4(self):
        for (host, ip)  in self.ip4Values:
            result = dns.ip4(host)
            self.assertEqual(ip, result)

class failures(unittest.TestCase):

    def testip4tostr(self):
        self.assertRaises(TypeError, dns.ip4tostr, 1234)
        self.assertRaises(TypeError, dns.ip4tostr, 1.2)
        self.assertRaises(TypeError, dns.ip4tostr, "1")
        self.assertRaises(TypeError, dns.ip4tostr, "12")
        self.assertRaises(TypeError, dns.ip4tostr, "123")
        self.assertRaises(TypeError, dns.ip4tostr, "12345")

unittest.main() 
