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
from dns.cache import RecordCache
from dns.resource import ResourceRecord


class Resolver:
    """DNS resolver"""

    def __init__(self, timeout, caching, ttl):
        """Initialize the resolver

        Args:
            caching (bool): caching is enabled if True
            ttl (int): ttl of cache entries (if > 0)
        """
        self.cache = RecordCache(10000000)
        self.timeout = timeout
        self.caching = caching
        self.ttl = ttl
        self.hints = {
            "a.root-servers.net":"198.41.0.4",
            "b.root-servers.net":"192.228.79.201",
            "c.root-servers.net":"192.33.4.12",
            "d.root-servers.net":"199.7.91.13",
            "e.root-servers.net":"192.203.230.10",
            "f.root-servers.net":"192.5.5.241",
            "g.root-servers.net":"192.112.36.4",
            "h.root-servers.net":"128.63.2.53",
            "i.root-servers.net":"192.36.148.17",
            "j.root-servers.net":"192.58.128.30",
            "k.root-servers.net":"193.0.14.129",
            "l.root-servers.net":"199.7.83.42",
            "m.root-servers.net":"202.12.27.33"}


    def gethostbyname(self, hostname):
        """Translate a host name to IPv4 address.

        Currently this method contains an example. You will have to replace
        this example with the algorithm described in section 5.3.3 in RFC 1034.

        Args:
            hostname (str): the hostname to resolve

        Returns:
            (str, [str], [str]): (hostname, aliaslist, ipaddrlist)
        """
        #start with empty lists
        aliaslist = []
        ipaddrlist = []
        #initiate with the list of hints to use.
        servers = self.hints.copy()
        #so hostname is not lost when we resolve a CNAME at some point.
        domain = hostname
        finished = False
        #check cache of hostname is in the cache.
        cache_entries = self.cache.lookup(hostname, Type.A, Class.IN) + self.cache.lookup(hostname, Type.CNAME, Class.IN)
        if(len(cache_entries) > 0):
            #TODO            
            pass
        while(servers and not finished):
            #take a server from the list of servers to ask for the domain we're looking for.
            name, server = servers.popitem()
            #if the server doesn't have an address, resolve this address first.
            if(server == None):
                a,b,c = self.gethostbyname(name)
                if(len(c)>0):
                    servers[name] = c[0]
                    server = c[0]
                else:
                    continue
            #check whether the name is in the cache.            
            cache_entries = self.cache.lookup(name, Type.A, Class.IN) + self.cache.lookup(name, Type.CNAME, Class.IN)
            if(len(cache_entries) > 0):
                for ce in cache_entries:
                    if ce.type_ == 1:
                        address = ans.rdata.to_dict()['address']
                        if(address not in ipaddrlist):
                            ipaddrlist.append(address)
                    if ce.type_ == 5:
                        domain = ans.to_dict()['rdata']['cname']
                        if domain not in aliaslist:
                            aliaslist.append(str(domain))
            #send question to the server to see if it knows where we can find domain
            try:
                response = self.sendQuestion(domain, server)
            except:
                continue
            #if the location is in the answers we're done.
            for ans in response.answers:
                if ans.type_ == 1:
                    address = ans.rdata.to_dict()['address']
                    if(address not in ipaddrlist):
                        ipaddrlist.append(address)
                        if(self.caching):
                            self.cache.add_record(ans)
                if ans.type_ == 5:
                    domain = ans.to_dict()['rdata']['cname']
                    if domain not in aliaslist:
                        aliaslist.append(str(domain))
            #add new servers we can ask for the location to our list of servers.
            new_servers = self.getNewServers(response.authorities, response.additionals)
            #if we found a (list of) IP-address(es) we're done.
            if(len(ipaddrlist) > 0):
                finished = True
            #combine old list of servers with new one.
            servers = {**servers, **new_servers}
        return hostname, aliaslist, ipaddrlist

    '''Used to combine the suggested servers to check. '''
    def getNewServers(self, authorities, additionals):
        serverlist = {}
        for b in authorities:
            if(b.type_ == 6):
                continue
            serverlist.update({str(b.rdata.to_dict()['nsdname']) : None})
            for a in additionals:
                if(str(a.name) == str(b.rdata.to_dict()['nsdname'])):
                    if(a.type_ == 1):
                        serverlist.update({str(b.rdata.to_dict()['nsdname']) : a.rdata.to_dict()['address']})
        return serverlist
                
    '''Used to handle the sending and receiving of requests/responses.'''
    def sendQuestion(self, hostname, server):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        # Create and send query
        identifier = 9001  # placeholder
        question = Question(Name(hostname), Type.A, Class.IN)
        header = Header(identifier, 0, 1, 0, 0, 0)
        header.qr = 0
        header.opcode = 0
        header.rd = 1
        query = Message(header, [question])
        sock.sendto(query.to_bytes(), (server, 53))

        # Receive response
        data = sock.recv(512)
        response = Message.from_bytes(data)
        sock.close()
        return response
