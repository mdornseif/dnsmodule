# $Id: _dnsmodule_test.py,v 1.1 2001/07/09 21:10:51 drt Exp $
#
# first steps to a testsuite for dnsmodule
# by drt - http://koeln.ccc.de/~drt/
#
# Todo: real tests of qualification
#       real tests of multiple responses
#       provoke lookup failures

import _dns
import unittest

class KnownValues(unittest.TestCase):
    
    ipValues =  [('',''),
                 ('127.0.0.1', '\x7f\x00\x00\x01'),
                 ('[127.0.0.1]', '\x7f\x00\x00\x01'),
                 ('127.0.0.1.127.0.0.1', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[127.0.0.1].[127.0.0.1]', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[127.0.0.1].127.0.0.1', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[127.0.0.1.127.0.0.1]', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[256.256.256.256]', '\x00\x00\x00\x00'),
                 ('[257.257.257.257]', '\x01\x01\x01\x01'),
                 ('[0.0.0.0]', '\x00\x00\x00\x00'),
                 ('[1.1.1.1]', '\x01\x01\x01\x01'),
                 ('dnstest.c0re.23.nu', '\x01\x02\x03-'),
                 ('none.dnstest.c0re.23.nu', ''),
                 ('broken.dnstest.c0re.23.nu', ''),
                 ('localhost', '\x7f\x00\x00\x01'),
                 ('ftp.porn.org', '\x7f\x00\x00\x01'),
                 ('www.example.com', '\x80\t\xb0 '),
                 ('a.root-servers.net', '\xc6)\x00\x04'),
                 ('b.root-servers.net', '\x80\t\x00k'),
                 ('c.root-servers.net', '\xc0!\x04\x0c'),
                 ('d.root-servers.net', '\x80\x08\nZ'),
                 ('e.root-servers.net', '\xc0\xcb\xe6\n'),
                 ('f.root-servers.net', '\xc0\x05\x05\xf1'),
                 ('g.root-servers.net', '\xc0p$\x04'),
                 ('h.root-servers.net', '\x80?\x025'),
                 ('i.root-servers.net', '\xc0$\x94\x11'),
                 ('k.root-servers.net', '\xc1\x00\x0e\x81'),
                 ('l.root-servers.net', '\xc6 @\x0c'),
                 ('m.root-servers.net', '\xca\x0c\x1b!')]
    ip_qualifyValues =  [('127.0.0.1', '\x7f\x00\x00\x01'),
                 ('[127.0.0.1]', '\x7f\x00\x00\x01'),
                 ('127.0.0.1.127.0.0.1', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[127.0.0.1].[127.0.0.1]', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[127.0.0.1].127.0.0.1', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[127.0.0.1.127.0.0.1]', '\x7f\x00\x00\x01\x7f\x00\x00\x01'),
                 ('[256.256.256.256]', '\x00\x00\x00\x00'),
                 ('[257.257.257.257]', '\x01\x01\x01\x01'),
                 ('[0.0.0.0]', '\x00\x00\x00\x00'),
                 ('[1.1.1.1]', '\x01\x01\x01\x01'),
                 ('dnstest.c0re.23.nu', '\x01\x02\x03-'),
                 ('none.dnstest.c0re.23.nu', ''),
                 ('broken.dnstest.c0re.23.nu', ''),
                 ('ftp.porn.org', '\x7f\x00\x00\x01'),
                 ('www.example.com', '\x80\t\xb0 '),
                 ('a.root-servers.net', '\xc6)\x00\x04'),
                 ('b.root-servers.net', '\x80\t\x00k'),
                 ('c.root-servers.net', '\xc0!\x04\x0c'),
                 ('d.root-servers.net', '\x80\x08\nZ'),
                 ('e.root-servers.net', '\xc0\xcb\xe6\n'),
                 ('f.root-servers.net', '\xc0\x05\x05\xf1'),
                 ('g.root-servers.net', '\xc0p$\x04'),
                 ('h.root-servers.net', '\x80?\x025'),
                 ('i.root-servers.net', '\xc0$\x94\x11'),
                 ('k.root-servers.net', '\xc1\x00\x0e\x81'),
                 ('l.root-servers.net', '\xc6 @\x0c'),
                 ('m.root-servers.net', '\xca\x0c\x1b!')]
    mxValues =  [('',''),
                 ('dnstest.c0re.23.nu', '\x00\x00mx.dnstest.c0re.23.nu\x00'),
                 ('multi.dnstest.c0re.23.nu', '\x00\x00mx.multi.dnstest.c0re.23.nu\x00\x00\x00mx.multi.dnstest.c0re.23.nu\x00\x00\x00mx.multi.dnstest.c0re.23.nu\x00\x00\x00mx.multi.dnstest.c0re.23.nu\x00\x00\x00mx.multi.dnstest.c0re.23.nu\x00\x00\x00mx.multi.dnstest.c0re.23.nu\x00\x00\x00mx.multi.dnstest.c0re.23.nu\x00\x00\x00mx.multi.dnstest.c0re.23.nu\x00'),
                 ('none.dnstest.c0re.23.nu', ''),
                 ('broken.dnstest.c0re.23.nu', ''),
                 ('localhost', ''),
                 ('ftp.porn.org', ''),
                 ('www.example.com', '\x00\x00venera.isi.edu\x00\x00\nboreas.isi.edu\x00'),
                 ('a.root-servers.net', '\x00\nrs.internic.net\x00'),
                 ('b.root-servers.net', ''),
                 ('c.root-servers.net', ''),
                 ('d.root-servers.net', '\x00\nnoc.umd.edu\x00'),
                 ('e.root-servers.net', '\x00\x05archimedes.nasa.gov\x00'),
                 ('f.root-servers.net', '\x00\nisrv3.pa.vix.com\x00'),
                 ('g.root-servers.net', '\x00\nnic.mil\x00'),
                 ('h.root-servers.net', ''),
                 ('i.root-servers.net', '\x00\x00server.nordu.net\x00'),]
    txtValues = [('',''),
                 ('dnstest.c0re.23.nu', 'testText'),
                 ('none.dnstest.c0re.23.nu', ''),
                 ('broken.dnstest.c0re.23.nu', ''),
                 ('localhost', ''),
                 ('ftp.porn.org', ''),
                 ('www.example.com', ''),
                 ('a.root-servers.net', 'formerly ns.internic.net'),
                 ('b.root-servers.net', 'formerly ns1.isi.edu'),
                 ('c.root-servers.net', 'formerly c.psi.net'),
                 ('d.root-servers.net', 'formerly terp.umd.edu'),
                 ('e.root-servers.net', 'formerly ns.nasa.gov'),
                 ('f.root-servers.net', 'formerly ns.isc.org'),
                 ('g.root-servers.net', 'formerly ns.nic.ddn.mil'),
                 ('h.root-servers.net', 'formerly aos.arl.army.mil'),
                 ('i.root-servers.net', 'formerly nic.nordu.net'),
                 ('k.root-servers.net', 'housed in LINX operated by RIPE NCC'),
                 ('l.root-servers.net', 'temporarily located at ISI'),
                 ('m.root-servers.net', 'housed in JAPAN operated by WIDE')]
    name4Values = [('\x00\x00\x00\x00', ''), 
                   ('\x7f\x00\x00\x01', 'localhost'), # localhost
                   ('\x7f\x00\x00\x02', ''), 
                   ('\x80\t\xb0 ', 'venera.isi.edu'), # www.example.com
                   ('\xc6)\x00\x04', 'a.root-servers.net'), # a.root-servers.net
                   ('\x80\t\x00k', 'b.root-servers.net'), # b.root-servers.net
                   ('\xc0!\x04\x0c', 'c.root-servers.net'), # c.root-servers.net
                   ('\x80\x08\nZ', 'd.root-servers.net'), # d.root-servers.net
                   ('\xc0\xcb\xe6\n', 'e.root-servers.net'), # e.root-servers.net
                   ('\xc0\x05\x05\xf1', 'f.root-servers.net'), # f.root-servers.net
                   ('\xc0p$\x04', 'g.root-servers.net'), # g.root-servers.net
                   ('\x80?\x025', 'h.root-servers.net'), # h.root-servers.net
                   ('\xc0$\x94\x11', 'i.root-servers.net'), # i.root-servers.net
                   ('\xc1\x00\x0e\x81', 'k.root-servers.net'), # k.root-servers.net
                   ('\xc6 @\x0c', 'l.root-servers.net'), # l.root-servers.net
                   ('\xca\x0c\x1b!', 'm.root-servers.net') # m.root-servers.net
                   ]

    def testipCase(self):
        for (host, ip)  in self.ipValues:
            result = _dns.ip4(host)
            self.assertEqual(ip, result)

    def testip_qualifyCase(self):
        for (host, ip)  in self.ip_qualifyValues:
            result = _dns.ip4_qualify(host)
            self.assertEqual((host, ip), result)

    def testmxCase(self):
        for (host, mx)  in self.mxValues:
            result = _dns.mx(host)
            self.assertEqual(mx, result)

    def testtxtCase(self):
        for (host, txt)  in self.txtValues:
            result = _dns.txt(host)
            self.assertEqual(txt, result)

    def testname4Case(self):
        for (ip, name)  in self.name4Values:
            result = _dns.name4(ip)
            self.assertEqual(name, result)

    def shortDescription(self):
        return 'Tests with known Hosts'

class badInput(unittest.TestCase):

    def testname4(self):
        self.assertRaises(TypeError, _dns.name4, '1')
        self.assertRaises(TypeError, _dns.name4, '12')
        self.assertRaises(TypeError, _dns.name4, '123')
        self.assertRaises(TypeError, _dns.name4, '1.2.3.4')
        self.assertRaises(TypeError, _dns.name4, 1234)
        self.assertRaises(TypeError, _dns.name4, 1.2)

    def testip4(self):
        self.assertRaises(TypeError, _dns.ip4, 1234)
        self.assertRaises(TypeError, _dns.ip4, 1.2)

    def testip4_qualify(self):
        self.assertRaises(TypeError, _dns.ip4_qualify, 1234)
        self.assertRaises(TypeError, _dns.ip4_qualify, 1.2)

    def testrandom_init(self):
        _dns.random_init('irgendwas')

    def shortDescription(self):
        return 'Tests with bad input'

           
unittest.main() 
