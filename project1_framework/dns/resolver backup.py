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
        self.cache = RecordCache(100)
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
        fqdn = hostname.split(".")
        if "" in fqdn:
            fqdn.remove("")
        record_dict = self.cache.lookup(hostname, Type.A, Class.IN)
        if (record_dict != None):
            resource_record = ResourceRecord.from_dict(record_dict)
            return (hostname, [], [resource_record.rdata.address])

        return self.resolveQuestion(fqdn, self.hints, 1)

    def resolveQuestion(self, fqdn, servers, iteration):
        ips = []
        aliass = []
        new_servers = {}
        servers = servers.copy()
        while(servers):
            name, server = servers.popitem()
            if(server == None):
                name2 = name.split(".")
                if("" in name2):
                    name2.remove("")
                (a,b,c) = self.resolveQuestion(name2, self.hints, 1)
                if(len(c) > 0):
                    new_servers[name] = c[0]
                    server = new_servers[name]
                else:
                    continue
#            print("Question: ", ".".join(fqdn[-iteration:]), " , to : " , name,  server)
            response = self.sendQuestion(".".join(fqdn[-iteration:]), server)
            if(len(response.answers) > 0):
                for ans in response.answers:
                    #Answer type == A, host server
                    if(ans.type_ == 1):
                        address = ans.rdata.to_dict()['address']
                        if(address not in ips):
                            ips.append(address)
                            if(self.caching):
                                self.cache.add_record(ans)
                    #Answer type == CNAME, canonical name
                    if(ans.type_ == 5):
                        newname = ans.to_dict()['rdata']['cname']
                        aliass.append(str(newname))
                        fqdn = str(newname).split(".")
                        if("" in fqdn):
                            fqdn.remove("")
                        return self.resolveQuestion(fqdn, self.hints, 1)
            else:
                new_servers.update(self.getNewServers2(response.authorities, response.additionals))
        if(iteration < len(fqdn)):                
            iteration = iteration + 1
        if(len(new_servers) > 0):
            return self.resolveQuestion(fqdn, new_servers, iteration)
        return (".".join(fqdn), aliass, ips)

    '''Couples authorities and additionals.'''
    def getNewServers(self, authorities, additionals):
        serverlist = {}
        for a in additionals:
            for b in authorities:
                if(str(a.name) == str(b.rdata.to_dict()['nsdname'])):
                    if(a.type_ == 1):
                        serverlist.update({str(a.name): a.rdata.to_dict()['address']})
        return serverlist

    def getNewServers2(self, authorities, additionals):
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
