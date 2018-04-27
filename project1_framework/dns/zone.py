#!/usr/bin/env python3

"""Zones of domain name space

See section 6.1.2 of RFC 1035 and section 4.2 of RFC 1034.
Instead of tree structures we simply use dictionaries from domain names to
zones or record sets.

These classes are merely a suggestion, feel free to use something else.
"""

from dns.resource import ResourceRecord
from dns.resource import ARecordData
from dns.resource import CNAMERecordData

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
        temp = {}
        """Read the cache file from disk"""
        with open("roothints.md") as file_:
            lines = file_.readlines()
        for l in lines:
            contents = l.split(" ")
            if(contents[0] == ";"):
                continue
            #First item is fqdn, second is a rr
            if("." in contents[0]):
                name = contents[0]
                class_ = 1
                if(isinstance(contents[1], int)):
                    ttl = contents[1]
                    type_ = contents[2]
                elif(isinstance(contents[1], str)):
                    ttl = contents[2]
                    type_ = contents[1]
                    rdata = contents[3]
                if(type_ == 1):
                    rdata = ARecordData(contents[3])
                if(type_ == 5):
                    rdata = CNAMERecordData(contents[3])
                rr = ResourceRecord(name, type_, class_, ttl, rdata)
                temp.update({name:rr})
        self.records = temp.copy()





