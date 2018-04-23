#!/usr/bin/env python3

"""A cache for resource records

This module contains a class which implements a cache for DNS resource records,
you still have to do most of the implementation. The module also provides a
class and a function for converting ResourceRecords from and to JSON strings.
It is highly recommended to use these.
"""


import json
import datetime
from datetime import timedelta

from dns.resource import ResourceRecord


class RecordCache:
    """Cache for ResourceRecords"""

    def __init__(self, ttl):
        """Initialize the RecordCache

        Args:
            ttl (int): TTL of cached entries (if > 0)
        """
        self.records = []
        self.ttl = ttl

    def lookup(self, dname, type_, class_):
        """Lookup resource records in cache

        Lookup for the resource records for a domain name with a specific type
        and class.

        Args:
            dname (str): domain name
            type_ (Type): type
            class_ (Class): class
        """
        print("Checking cache...", len(self.records))
        for r in self.records:
            r = r.to_dict()
            print(r.name, dname)
            if(r['name'] == dname and r['type'] == type_ and r['class'] == class_):
                if(r['ttl'] > datetime.datetime.now()):
                    return ResourceRecord.from_dict(r)
                else:
                    records.remove(r.from_dict())
        return (None)

    def add_record(self, record):
        """Add a new Record to the cache

        Args:
            record (ResourceRecord): the record added to the cache
        """
        print("Adding to cache...")
        record = record.to_dict()
        now = datetime.datetime.now()
        end = self.addSecs(now, self.ttl)
        if self.ttl > 0:
            record['ttl'] = end
        self.records.append(ResourceRecord.from_dict(record))

    def read_cache_file(self):
        """Read the cache file from disk"""
        dcts = []
        try:
            with open("cache", "r") as file_:
                dcts = json.load(file_)
        except:
            print("could not read cache")
        self.records = [ResourceRecord.from_dict(dct) for dct in dcts]

    def write_cache_file(self):
        """Write the cache file to disk"""
        dcts = [record.to_dict() for record in self.records]
        try:
            with open("cache", "w") as file_:
                json.dump(dcts, file_, indent=2)
        except:
            print("could not write cache")

    def addSecs(self, tm, secs):
        return tm + timedelta(seconds=secs)
