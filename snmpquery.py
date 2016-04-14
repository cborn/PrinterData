"""
querysnmp.py  Kiya Govek  2015 Jan
populates information holding objects from printerclass.py
with information from snmp queries to printers
"""

from printerclass import *
# pysnmp provides a format to use snmp with python
from pysnmp.hlapi import *
import pysnmp

# Runs through OIDs starting at 1.3.6.1.2.1.43.8.2.1.10.1.1 until reaches non-paper-level OID
# Returns list of paper level values, order corresponds to tray order
def paper_level(IP):
    trays = []
    for errorIndication, \
        errorStatus, errorIndex, \
        varBinds in nextCmd(SnmpEngine(),
                            CommunityData('public', mpModel=0),
                            UdpTransportTarget((IP, 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity('1.3.6.1.2.1.43.8.2.1.10.0'))):
        if errorIndication:
            return ['error',errorIndication.__str__()]
        elif errorStatus:
            return ['error','%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                )]
        else:
            for varBind in varBinds:
                oid = varBind[0]
                val = varBind[1]
                if tuple(oid)[-3] != 10:
                    return trays
                trays.append(val)

# Runs through OIDs starting at 1.3.6.1.2.1.43.8.2.1.12.1.1 until reaches non-paper-type OID
# Returns list of paper type values, order corresponds to tray order
def paper_type(IP):
    trays = []
    for errorIndication, \
        errorStatus, errorIndex, \
        varBinds in nextCmd(SnmpEngine(),
                            CommunityData('public', mpModel=0),
                            UdpTransportTarget((IP, 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity('1.3.6.1.2.1.43.8.2.1.12.0'))):
        if errorIndication:
            return ['error',errorIndication.__str__()]
        elif errorStatus:
            return ['error','%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                )]
        else:
            for varBind in varBinds:
                oid = varBind[0]
                val = varBind[1]
                if tuple(oid)[-3] != 12:
                    return trays
                trays.append(val)

# Runs through OIDs starting at 1.3.6.1.2.1.43.11.1.1.8.1.1, until reaches non-toner-level OID
# First half are toner max values, second half are toner actual values
# Returns list of toner level values, order corresponds to toner order
def toner_level(IP):
    toners = []
    for errorIndication, \
        errorStatus, errorIndex, \
        varBinds in nextCmd(SnmpEngine(),
                            CommunityData('public', mpModel=0),
                            UdpTransportTarget((IP, 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.0'))):
        if errorIndication:
            return ['error',errorIndication.__str__()]
        elif errorStatus:
            return ['error','%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                )]
        else:
            for varBind in varBinds:
                oid = varBind[0]
                val = varBind[1]
                if tuple(oid)[-6] != 11:
                    return toners
                toners.append(val)

# Checks disabled status of printer, starting with the first OID 1.3.6.1.2.1.43.18.1.1.2.1.__
# where __ may be any number. 
# Goes until reaches error disabling printer or non-error OID, returns disabled status of printer
def status(IP):
    for errorIndication, \
        errorStatus, errorIndex, \
        varBinds in nextCmd(SnmpEngine(),
                            CommunityData('public', mpModel=0),
                            UdpTransportTarget((IP, 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity('1.3.6.1.2.1.43.18.1.1.2.1'))):
        if errorIndication:
            return ['error',errorIndication.__str__()]
        elif errorStatus:
            return ['error','%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                )]
        else:
            for varBind in varBinds:
                oid = varBind[0]
                val = varBind[1]
                if tuple(oid)[-3] != 2 or tuple(oid)[-6] != 18:
                    return ['Ready',None]
                if val == 3:
                    return ['Printing is disabled',str(oid)]

# Takes an OID and returns the value associated with that OID
# Used after status returns a disabled message to check the error that disabled the printer
def error_message(IP, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
        SnmpEngine(),
        CommunityData('public',mpModel=0),
        UdpTransportTarget((IP, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))))
    
    if errorIndication:
        return ['error',errorIndication.__str__()]
    elif errorStatus:
        return ['error','%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[-1][int(errorIndex)-1] or '?'
            )
        ]
    else:
        for varbind in varBinds:
            val = varbind[1]
            return ['success',val.prettyPrint()]

# Returns the message displayed on the physical printer screen
def screen_message(IP):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
        SnmpEngine(),
        CommunityData('public',mpModel=0),
        UdpTransportTarget((IP, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.43.16.5.1.2.1.1'))))
    
    if errorIndication:
        return ['error',errorIndication.__str__()]
    elif errorStatus:
        return ['error','%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[-1][int(errorIndex)-1] or '?'
            )
        ]
    else:
        for varbind in varBinds:
            val = varbind[1]
            return ['success',val.prettyPrint()]

