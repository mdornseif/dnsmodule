#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name="dnsmodule",
      version="0.1test",
      description="Python DNS Module",
      author="drt",
      author_email="drt@un.bewaff.net",
      url="http://c0re.jp/c0de/dnsmodule/",
      ext_modules=[Extension("foo", ["foo.c"])]
      )

