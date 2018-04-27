import re
from dns.resource import ResourceRecord
from dns.resource import ARecordData
from dns.resource import NSRecordData
from dns.resource import CNAMERecordData
from dns.types import Type
from dns.classes import Class

def getType(t):
    if(t == 'A'):
        return Type.A
    if(t == 'NS'):
        return Type.NS
    if(t == 'CNAME'):
        return Type.CNAME

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
        type_ = getType(te[2])
        if(type_ == Type.A):
            rdata = ARecordData(te[3])
        elif(type_ == Type.NS):
            rdata = NSRecordData(te[3])
        elif(type_ == Type.CNAME):
            rdata = CNAMERecordData(te[3])
        rr = ResourceRecord(te[0], type_, Class.IN, te[1], rdata)
        print(rr.to_dict())

    
