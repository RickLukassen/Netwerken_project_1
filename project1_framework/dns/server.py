#!/usr/bin/env python3

"""A recursive DNS server

This module provides a recursive DNS server. You will have to implement this
server using the algorithm described in section 4.3.2 of RFC 1034.
"""

import socket


from threading import Thread
from dns.zone import Zone
from dns.message import Message, Question, Header


class RequestHandler(Thread):
    """A handler for requests to the DNS server"""

    def __init__(self):
        """Initialize the handler thread"""
        super().__init__()
        self.daemon = True

    def run(self):
        """ Run the handler thread"""
        pass


class Server:
    """A recursive DNS server"""

    def __init__(self, port, caching, ttl):
        """Initialize the server

        Args:
            port (int): port that server is listening on
            caching (bool): server uses resolver with caching if true
            ttl (int): ttl for records (if > 0) of cache
        """
        self.caching = caching
        self.ttl = ttl
        self.port = port
        self.done = False

    def serve(self):
        """Start serving requests"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        sock.bind(('localhost', self.port))
        zone = Zone().read_master_file("roothints.md")
        #load zone file into memory
        while not self.done:
            print("Waiting...")
            data, address = sock.recvfrom(512)
            #Following piece of code results in a weird error message which I do not understand. I do quite literally the same thing some other students do but it results in an error message.
            req = Message.from_bytes(data)
            questions = req.questions
            for question in questions:
                hostname = question.qname
                
                #consult zone and try to answer and cache
                #if recursion is enabled, and zone does not help: use resolver
            #send back reply.
            pass

    def shutdown(self):
        """Shut the server down"""
        self.done = True
