/* Low Level Interface to Dan Bernsteins djbdns library
   see http://cr.yp.to/djbdns.html

   D. R. Tzeck - http://koeln.ccc.de/~drt/
*/

static char rcsid[] = "$Id: _dnsmodule.c,v 1.1 2001/07/09 21:10:50 drt Exp $";
   
#include <Python.h>
#include "djb/dns.h"

static char module_Doc[] = "dns - python bindings to Dan Bernsteins DNS Library.

Dan Bernstein provides with his djbdns domain name server toolkit
a high quality implementation of a DNS client library. See
http://cr.yp.to/djbdns/dns.html .This bindings allow to acces
this library from python and build high level functions on top of
it.

Transmission details

The dns_ip4, dns_ip4_qualify, dns_name4, dns_mx, and dns_txt
functions are DNS clients (sometimes called ``stub
resolvers''). They send recursive DNS queries to a nearby DNS
cache.

Normally the IP address of the DNS cache is listed on a
nameserver line in /etc/resolv.conf. If /etc/resolv.conf does not
exist or does not list any IP addresses, these functions send
queries to the local host, 127.0.0.1.

/etc/resolv.conf is automatically reread after 10 minutes or
10000 uses. Beware that this feature is not supported by most DNS
client libraries.

The user can override /etc/resolv.conf by setting the $DNSCACHEIP
environment variable. Beware that this feature is not supported
by most DNS client libraries.
";

/* Helper Function missing from djbdns */
void static stralloc_free(stralloc *sa)
{
  alloc_free(sa->s);
  sa->s = 0;
  sa->len = sa->a = 0;
}


/* Interface to dns_ip4 */
static char ip4_Doc[] = "ip(fqdn) - look up fully qualified domain name. 

ip4 looks up 4-byte IP addresses for the fully-qualified
domain name in the string fqdn. It returns the binary
concatenation of the IP addresses. If the domain does not exist
in DNS, or has no IP addresses, the returned value will be empty.

If dns_ip4 has trouble with the DNS lookup, it will raise
LookupError.

If fqdn is a dotted-decimal IP address, ip4 puts that IP
address into out without checking DNS. More generally, if fqdn is
a dot-separated sequence of dotted-decimal IP addresses, ip4
puts those IP addresses into out without checking DNS. Brackets
may appear inside the dotted-decimal IP addresses; they are
ignored.";

static PyObject *ip4(self, args)
     PyObject *self;
     PyObject *args;
{
  PyObject *ret;
  char *fqdn;
  static stralloc sa_fqdn = {0};
  static stralloc sa_out = {0};
  
  if(!PyArg_ParseTuple(args, "s", &fqdn))
    return NULL;
  
  if(!stralloc_copys(&sa_fqdn, fqdn))
    {
      stralloc_free(&sa_fqdn);
      return PyErr_NoMemory();
    }
  
  if(dns_ip4(&sa_out, &sa_fqdn) == -1)
    {
      stralloc_free(&sa_fqdn);
      stralloc_free(&sa_out);
      return PyErr_SetFromErrno(PyExc_LookupError);
    }

  ret = Py_BuildValue("s#", sa_out.s, sa_out.len);
  stralloc_free(&sa_fqdn);
  stralloc_free(&sa_out);
  return ret;
}



/* interface to dns_ip4_qualify */

static char ip4_qualify_Doc[] = "ip4_qualify(dn) - takes a domain name as a string, puts it
through a qualification process and looks up assosiated IP
Adresses.

dns_ip4_qualify feeds the name dn through qualification and looks
up 4-byte IP addresses for the result. It returns a tuple
consisting of the fully qualified domain name and the binary
concatenation of the IP addresses as a string. If the domain does
not exist in DNS, or has no IP addresses, this string will be
empty.

If dns_ip4_qualify has trouble with the qualification, has
trouble with DNS, it raises LookupError.

Qualification means conversion of a short host name, such as
cheetah, into a complete (``fully qualified'') domain name, such
as cheetah.heaven.af.mil.

This page explains the qualification rules followed by the
dns_ip4_qualify library routine in djbdns.

Rewriting instructions

Normally dns_ip4_qualify follows instructions listed in
/etc/dnsrewrite. You can override these instructions by creating
your own file and setting the $DNSREWRITEFILE environment
variable to the name of that file.

Sample instructions:

     # anything.local -> me
     -.local:me
     # me -> 127.0.0.1
     =me:127.0.0.1
     # any.name.a -> any.name.af.mil
     *.a:.af.mil
     # any-name-without-dots -> any-name-without-dots.heaven.af.mil
     ?:.heaven.af.mil
     # remove trailing dot
     *.:

Instructions are followed in order, each at most once. There are
four types of instructions:


 =post:new means that the host name post is replaced by new.
 *post:new means that any name of the form prepost is replaced by prenew.
 ?post:new means that any name of the form prepost, where pre does not contain dots or brackets, is replaced by prenew.
 -post:new means that any name of the form prepost is replaced by new.


Searching

dns_ip4_qualify can search through DNS for several possible
qualifications of a name. For example, the name

     cheetah+.heaven.af.mil+.af.mil

is qualified as cheetah.heaven.af.mil if that name has IP
addresses listed in DNS, or cheetah.af.mil otherwise.

In general, x+y1+y2+y3 is qualified as xy1 if xy1 has IP
addresses listed in DNS; otherwise, as xy2 if xy2 has IP
addresses listed in DNS; otherwise, as xy3. You can list any
number of +'s.

Searching is applied after rewriting, so you can use a rewriting
instruction such as

     ?:+.heaven.af.mil+.af.mil

to have lion qualified as lion.heaven.af.mil or lion.af.mil, and
tiger qualified as tiger.heaven.af.mil or tiger.af.mil, and so
on.

Searching is generally not a recommended feature. If you rely on
gw being qualified as gw.af.mil, and someone suddenly adds a new
gw.heaven.af.mil, you'll end up talking to the wrong host. It's
better to rely on syntactic rules that you control.


Compatibility mechanisms

If the rewriting-instructions file does not exist,
dns_ip4_qualify looks for a local domain name in three places:

1.the $LOCALDOMAIN environment variable, if it is set; or
2.the first domain or search line in /etc/resolv.conf, if /etc/resolv.conf exists and has such a line; or
3.everything after the first dot in the system's hostname.

It then creates rewriting instructions of the form

     ?:.domain
     *.:

so that .domain is added to any name without dots or brackets.

You can specify searching in $LOCALDOMAIN by using several domain
names separated by spaces. Your system administrator can specify
searching in /etc/resolv.conf by putting several domains on a
search
";

static PyObject *ip4_qualify(self, args)
     PyObject *self;
     PyObject *args;
{
  PyObject *ret;
  char *dn;
  static stralloc sa_dn = {0};
  static stralloc sa_fqdn = {0};
  static stralloc sa_out = {0};
  
  if(!PyArg_ParseTuple(args, "s", &dn))
    return NULL;
  
  if(!stralloc_copys(&sa_dn, dn))
    {
      stralloc_free(&sa_dn);
      return PyErr_NoMemory();
    }
  
  if(dns_ip4_qualify(&sa_out, &sa_fqdn, &sa_dn) == -1)
    {
      stralloc_free(&sa_dn);
      stralloc_free(&sa_fqdn);
      stralloc_free(&sa_out);
      return PyErr_SetFromErrno(PyExc_LookupError);
    }
  
  ret = Py_BuildValue("s#s#", sa_fqdn.s, sa_fqdn.len, sa_out.s, sa_out.len);
  stralloc_free(&sa_dn);
  stralloc_free(&sa_fqdn);
  stralloc_free(&sa_out);
  return ret;
}



/* Interface to dns_mx */

static char mx_Doc[] = "mx(fqdn) - look up MX Records for Domain fqdn.

mx looks up MX records for the fully-qualified domain name in
fqdn. It returns the MX records as a string. Each MX record is a
two-byte MX distance followed by a \0-terminated dot-encoded
domain name. If the domain does not exist in DNS, or has no MX
records, the return value will be empty.

If mx has trouble with the DNS lookup, it raises LookupError.
";

static PyObject *mx(self, args)
     PyObject *self;
     PyObject *args;
{
  PyObject *ret;
  char *fqdn;
  static stralloc sa_fqdn = {0};
  static stralloc sa_out = {0};
  
  if(!PyArg_ParseTuple(args, "s", &fqdn))
    return NULL;
  
  if(!stralloc_copys(&sa_fqdn, fqdn))
    {
      stralloc_free(&sa_fqdn);
      return PyErr_NoMemory();
    }
  
  if(dns_mx(&sa_out, &sa_fqdn) == -1)
    {
      stralloc_free(&sa_fqdn);
      stralloc_free(&sa_out);
      return PyErr_SetFromErrno(PyExc_LookupError);
    }

  ret = Py_BuildValue("s#", sa_out.s, sa_out.len);
  stralloc_free(&sa_fqdn);
  stralloc_free(&sa_out);
  return ret;
}



static char txt_Doc[] = "txt(fqdn) - return TXT records for fqdn.

txt looks up TXT records for the fully-qualified domain name in
fqdn. It returns the concatenation of the TXT records. If the
domain does not exist in DNS, or has no TXT records, the return
value will be empty.

If txt has trouble with the DNS lookup it wil raise LookupError.
";

static PyObject *txt(self, args)
     PyObject *self;
     PyObject *args;
{
  PyObject *ret;
  char *fqdn;
  static stralloc sa_fqdn = {0};
  static stralloc sa_out = {0};
  
  if(!PyArg_ParseTuple(args, "s", &fqdn))
    return NULL;
  
  if(!stralloc_copys(&sa_fqdn, fqdn))
    {
      stralloc_free(&sa_fqdn);
      return PyErr_NoMemory();
    }
  
  if(dns_txt(&sa_out, &sa_fqdn) == -1)
    {
      stralloc_free(&sa_fqdn);
      stralloc_free(&sa_out);
      return PyErr_SetFromErrno(PyExc_LookupError);
    }

  ret = Py_BuildValue("s#", sa_out.s, sa_out.len);
  stralloc_free(&sa_out);
  return ret;
}

static char name4_Doc[] = "name4(ip) - get fully qualified domain name to an IP address.

name4 looks up the domain name for the 4-byte binary IP address
in the string ip. It returns the (first) domain name. If the
relevant in-addr.arpa domain does not exist in DNS, or has no PTR
records, the return value will be empty.

If name4 has trouble with the DNS lookup, it raises LookupError.
";

static PyObject *name4(self, args)
     PyObject *self;
     PyObject *args;
{
  PyObject *ret;
  char *ip;
  int size;
  static stralloc sa_out = {0};
  
  if(!PyArg_ParseTuple(args, "s#", &ip, &size))
    return NULL;

  if(size != 4)
    {
      PyErr_SetString(PyExc_TypeError,
		      "string containing IP data must be exactly 4 bytes long");
      return NULL;
    }
  
  if(dns_name4(&sa_out, ip) == -1)
    {
      stralloc_free(&sa_out);
      return PyErr_SetFromErrno(PyExc_LookupError);
    }

  ret = Py_BuildValue("s#", sa_out.s, sa_out.len);
  stralloc_free(&sa_out);
  return ret;
}

static char random_init_Doc[] = "random_init(seed) initializes the pseudorandom number generator.

random_init initializes the pseudorandom number generator used
through the dns library, taking account of seed, the current
process ID, and the current time.

Seed can be a string of any size but should contain at least 128
bytes if you want to gather maximum entropy.

Notes on DNS query security

A DNS client will accept any response that shows up at the right
time, is addressed from the IP address of the legitimate server,
is addressed to the UDP port used in the DNS query, repeats the
query name and type used in the DNS query, and repeats the 16-bit
ID used in the DNS query.

An active sniffing attacker can easily forge responses by copying
information from queries. Blind attackers need to guess the time,
UDP port, and ID for the targeted query name.

The dns_transmit functions use dns_random to create query IDs and
UDP ports. The dns_random generator is designed to be extremely
difficult to predict for an attacker who cannot guess seed. Note,
however, that there are only about a billion possible ID-port
pairs, so a prolonged blind attack will succeed eventually.
";

static PyObject *random_init(self, args)
     PyObject *self;
     PyObject *args;
{
  char *ent;
  int size;
  char seed[128];
  char *r, *w;
  
  if(!PyArg_ParseTuple(args, "t#", &ent, &size))
    return NULL;
  
  for(r = ent, w = seed; r < ent + size; r++, w++)
    {
      if(w >= seed + 128)
	w = seed;
      *w ^= *r;
    }
  
  dns_random_init(seed);

  return Py_None;
}




static PyMethodDef dnsMethods[] = {
      {"ip4",         ip4,         METH_VARARGS, ip4_Doc},
      {"ip4_qualify", ip4_qualify, METH_VARARGS, ip4_qualify_Doc},
      {"mx",          mx,          METH_VARARGS, mx_Doc},
      {"txt",         txt,         METH_VARARGS, txt_Doc},
      {"name4",       name4,       METH_VARARGS, name4_Doc},
      {"random_init", random_init, METH_VARARGS, random_init_Doc},
      {NULL,      NULL}        /* Sentinel */
};

void init_dns()
{
  (void) Py_InitModule3("_dns", dnsMethods, module_Doc);
}


