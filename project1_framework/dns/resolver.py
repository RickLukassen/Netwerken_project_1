#!/usr/bin/env python3

"""DNS Resolver

This module contains a class for resolving hostnames. You will have to implement
things in this module. This resolver will be both used by the DNS client and the
DNS server, but with a different list of servers.
"""


import socket

from dns.classes import Class
from dns.message import Message, Question, Header
from dns.name import Name
from dns.types import Type


class Resolver:
    """DNS resolver"""

    def __init__(self, timeout, caching, ttl):
        """Initialize the resolver

        Args:
            caching (bool): caching is enabled if True
            ttl (int): ttl of cache entries (if > 0)
        """
        self.timeout = timeout
        self.caching = caching
        self.ttl = ttl

    def gethostbyname(self, hostname):
        """Translate a host name to IPv4 address.

        Currently this method contains an example. You will have to replace
        this example with the algorithm described in section 5.3.3 in RFC 1034.

        Args:
            hostname (str): the hostname to resolve

        Returns:
            (str, [str], [str]): (hostname, aliaslist, ipaddrlist)
        """
        hints = [
            "198.41.0.4",
            "192.228.79.201",
            "192.33.4.12",
            "199.7.91.13",
            "192.203.230.10",
            "192.5.5.241",
            "192.112.36.4",
            "128.63.2.53",
            "192.36.148.17",
            "192.58.128.30",
            "193.0.14.129",
            "199.7.83.42",
            "202.12.27.33"]

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        # check if hostname is in local data
        # todo

        finished = False
        query_id = 1
        # Create and send query
        while(not(finished) and hints):
            question = Question(Name(hostname), Type.A, Class.IN)
            header = Header(query_id, 0, 1, 0, 0, 0)
            header.qr = 0
            header.opcode = 0
            header.rd = 1
            query = Message(header, [question])
            server = hints.pop([0])
            sock.sendto(query.to_bytes(), (server, 53))

            # Receive response
            data = sock.recv(512)
            response = Message.from_bytes(data)

            # Get data and do stuff with it
            aliaslist = []
            ipaddrlist = []
            for answer in response.answers:
                #result we're looking for
                if answer.type_ == Type.A and answer.name == hostname:
                    ipaddrlist.append(answer.rdata.address)
                    #cache it, todo
                    finished = True
                #canonical name
                if answer.type_ == Type.CNAME:
                    aliaslist.append(hostname)
                    hostname = str(answer.rdata.cname)
                #other cases??
                #todo
                    
            query_id += 1
        return hostname, aliaslist, ipaddrlist
