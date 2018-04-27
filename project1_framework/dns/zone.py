#!/usr/bin/env python3

"""Zones of domain name space

See section 6.1.2 of RFC 1035 and section 4.2 of RFC 1034.
Instead of tree structures we simply use dictionaries from domain names to
zones or record sets.

These classes are merely a suggestion, feel free to use something else.
"""

import re
from dns.resource import ResourceRecord
from dns.resource import ARecordData
from dns.resource import NSRecordData
from dns.resource import CNAMERecordData
from dns.types import Type
from dns.classes import Class

class Catalog:
    """A catalog of zones"""

    def __init__(self):
        """Initialize the catalog"""
        self.zones = {}

    def add_zone(self, name, zone):
        """Add a new zone to the catalog

        Args:
            name (str): root domain name
            zone (Zone): zone
        """
        self.zones[name] = zone


class Zone:
    """A zone in the domain name space"""

    def __init__(self):
        """Initialize the Zone """
        self.records = {}

    def add_node(self, name, record_set):
        """Add a record set to the zone

        Args:
            name (str): domain name
            record_set ([ResourceRecord]): resource records
        """
        self.records[name] = record_set

    def read_master_file(self, filename):
        """Read the zone from a master file

        See section 5 of RFC 1035.

        Args:
            filename (str): the filename of the master file
        """
        temp = []
        """Read the cache file from disk"""
        with open("roothints.md") as file_:
            lines = file_.readlines()
        for l in lines:
            #remove comments
            b = re.sub(r';[^\n]*', "", l)
            te = l.split()
            if(te[0] != ';'):
                temp.append(te)
            if("." in te[0]):
                type_ = self.getType(te[2])
                if(type_ == Type.A):
                    rdata = ARecordData(te[3])
                elif(type_ == Type.NS):
                    rdata = NSRecordData(te[3])
                elif(type_ == Type.CNAME):
                    rdata = CNAMERecordData(te[3])
                rr = ResourceRecord(te[0], type_, Class.IN, te[1], rdata)
                self.records.update({te[0] : rr})

    def getType(self,t):
        if(t == 'A'):
            return Type.A
        if(t == 'NS'):
            return Type.NS
        if(t == 'CNAME'):
            return Type.CNAME





