#!/usr/bin/env python3

"""Tests for your DNS resolver and server"""


import sys
import unittest
from unittest import TestCase
from argparse import ArgumentParser
from dns.resolver import Resolver
from dns.cache import RecordCache
from dns.types import Type
from dns.classes import Class
from dns.resource import ResourceRecord
from dns.resource import ARecordData

PORT = 5001
SERVER = "localhost"


class TestResolver(TestCase):
    """Resolver tests"""
    def testResolver(self):
        res = Resolver(0, False, 0)
        self.assertEqual(res.gethostbyname("google.com")[0], "google.com")
        self.assertEqual(res.gethostbyname("symposium.thalia.nu")[2],res.gethostbyname("reis.thalia.nu")[2])


class TestCache(TestCase):
    """Cache tests"""
    def testCache(self):
        cac = RecordCache(0)
        self.assertEqual(cac.lookup("abcdefghqqqq.com", Type.A, Class.IN), [])
        test = ResourceRecord("blabla.com", Type.A, Class.IN, 0, ARecordData("111.111.111.111"))
        cac.add_record(test)
        self.assertEqual(cac.lookup("blabla.com", Type.A, Class.IN), test)

class TestResolverCache(TestCase):
    """Resolver tests with cache enabled"""


class TestServer(TestCase):
    """Server tests"""


def run_tests():
    """Run the DNS resolver and server tests"""
    parser = ArgumentParser(description="DNS Tests")
    parser.add_argument("-s", "--server", type=str, default="localhost",
                        help="the address of the server")
    parser.add_argument("-p", "--port", type=int, default=5001,
                        help="the port of the server")
    args, extra = parser.parse_known_args()
    global PORT, SERVER
    PORT = args.port
    SERVER = args.server

    # Pass the extra arguments to unittest
    sys.argv[1:] = extra

    # Start test suite
    unittest.main()


if __name__ == "__main__":
    run_tests()
