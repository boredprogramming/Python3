"""
Returned datatype = JSON with double quotes instead of single as it
causes some issues depening on how devices are configured and the data that comes back.
It may cause invalid JSON to be returned.

Add an additional file with a variable named "production_paths"
as a list where each entry is a list of any potential additional directories that you want
to add to the program to ensure all things run smoothly (Or if you didn't feel like correcting your system variables)
This can be modified to work with your DEV server as well if you have different instances of python / packages etc
"""
from additional_directories import production_paths
import sys
import os
import re
import argparse
import binascii
import json
import socket
import time
import hashlib
'''
Append the system path with where the script will be ran, This may differ
from computer (Test bed) to the deployed server.
'''
for path in production_paths:
    sys.path.append(path)

'''
ALLOW THE PROGRAM TO FIGURE OUT WHERE THE FILES TO OPEN ARE STORED
RELATIVE TO WHERE THE SCRIPT IS BEING CALLED FROM.

EG IF THIS IS RAN FROM YOUR HOME DIRECTORY PYTHON SEES A DIFFERENT PATH FOR FILES
EVEN IF THEY ARE STORED IN THE SAME DIRECTORY..

'''
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

"""
Import your own community strings in a separate library file. 
"""
from Python.Python3.packages.snmp_strings.snmp_community_strings import YOURCOMMUNITYSTRING

"""
Import your custom library file 
This will contain what you want to pull from a device. 
You will be able to choose the names of the data returned for each OID. 

The snmp OIDs should be in OID format, 
EG .1.3.6.1.2.1.31.1.1.1.1 and NOT IF-MIB::ifName
Due to PySNMPs library, It has some issues running with the other. 
I haven't had time to figure out why yet as i'm new to this package.
"""

from Python.Python3.packages.snmp_library.snmp_library_file import library

from pysnmp import hlapi
from pysnmp.hlapi import nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

from Python.Python3.packages.credentials.wr_creds import MY_DB_WRITE_CREDS
from mysql.connector import connect, Error
'''
arg parse configurations
'''

parser = argparse.ArgumentParser(description='Poll a device for it\'s information!')
parser.add_argument('-device', '--device', help='TID or IP of the device')

args = parser.parse_args()
device = args.device

'''
FUNCTIONS - BEGIN
'''
def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port), timeout=10.0, retries=0),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

def get_bulk(target, oids, credentials, start_from=0, port=161,
             engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        start_from,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                if str(error_indication) == 'No SNMP response received before timeout':
                    return False
                else:
                    raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

def cast(value):
    """
    Custom casting will go on top.
    For example, The SnmpEngineID MIB will return a bytes encoded string
    that will need to be encoded to a HEX string.

    This can be caught by the class name that is returned by pysnmp and
    converted from there.
    """
    if value.__class__.__name__ == 'SnmpEngineID':
        """
        Convert the bytes string that is returned from the snmp get
        to the appropriate HEX value that you would see in a normal snmp query. 
        
        Example data returned 
        b'\x80\x00\t\xf0\x03\x00\x80\xeab\xb7@'
        This should render
        800009f0030080ea62b740
        """
        binary_string = binascii.hexlify(bytes(value))
        return str(binary_string.decode("utf-8"))
    else:
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
    return value

def notification(data):
    data = data
    data = json.dumps(data)
    sys.stdout.write(data)
    sys.stdout.flush()
    sys.exit(0)
'''
FUNCTIONS - END
'''


'''
Where poller data will be stored. 
Init the dict
'''
poller_data = {}

'''
Try all the snmp communities in the provided list, stop when one returns the device type
May need to be adjusted for different devices, but the oid used is generally from the 
normal SNMP MIBs and not device specific   
'''
if device:
    print("Firing up the old poller...\n")
    ip_regex = r'^(([0-9]{1,3}\.){3}[0-9]{1,3})$'
    ip_regex = re.compile(ip_regex)
    ip_regex = ip_regex.search(device)

    tid_regex = r'^(\w{11})$'
    tid_regex = re.compile(tid_regex)
    tid_regex = tid_regex.search(device)


    if ip_regex:
        """
        An IP was passed in. 
        Attempt to retrieve the DNS Entry for the IP
        """
        device_ip = device
        try:
            device_tid = socket.gethostbyaddr(device)
            if device_tid[0]:
                device_tid = device_tid[0]
            proceed = True
        except:
            proceed = False
    elif tid_regex:
        """
        A TID was passed in. 
        Attempt to retrieve the IP for the device
        """
        try:
            device_ip = socket.gethostbyname(device)
            device_tid = device
            proceed = True
        except:
            proceed = False
    else:
        print("Invalid entry. An 11 character TID or management IP is required")

    if proceed:
        print("Trying {} - {}".format(device_ip, device_tid))

        poller_library = False

        for string in YOURCOMMUNITYSTRING.community:
            print("Trying string {}".format(string))
            '''
            Which ever string is allowed to poll, Set that as the string to use
            '''
            try:
                print("Trying \"{}\"".format(device_ip))
                information = get(device_ip, ['.1.3.6.1.2.1.1.1.0'], hlapi.CommunityData(string))
                print(information)
                """
                Regex for any specific portions of the device type. 
                This helps when there may be different types of replies from the same gear with different
                versions and you can point them all to the same library if applicable
                """
                if information:
                    allowed_string = string
                    for key, value in information.items():
                        print("{} :: {}".format(key, value))
                        device_type = value
                        device_type_save = value
                        print("Device type - > {}".format(device_type))
                        """
                        Un hash the following line to see what is returned from the OID .1.3.6.1.2.1.1.1.0 -> SNMPv2-MIB::sysDescr.0
                        """

                        """
                        Ciena regex
                        """
                        ciena_switch_regex = r'.*(oneos-standard machine|5171 Packetwave Platform).*$'
                        ciena_switch_regex = re.compile(ciena_switch_regex)
                        regex_check_ciena = ciena_switch_regex.search(device_type)
                        """
                        END Ciena regex
                        """

                        """
                        QFX-5100 / QFX5110 regex
                        """
                        qfx_regex = r'.*(qfx5100|qfx5110).*'
                        qfx_regex = re.compile(qfx_regex)
                        regex_check_qfx = qfx_regex.search(device_type)
                        """
                        END QFX-5100 / QFX5110 regex
                        """

                        if regex_check_ciena:
                            device_type = "CIENA_SWITCH"
                            poller_library = library(device_type)
                        elif regex_check_qfx:
                            device_type = "QFX-51XX"
                            poller_library = library(device_type)
                        else:
                            poller_library = library(device_type)
                    break
            except:
                allowed_string = "None"

        '''
        This section will deal with the library's snmpget values ['get']
        '''
        if poller_library:
            """
            SNMP GET
            """
            for description, oid in poller_library['get'].items():
                poller_information = get(device_ip, [oid], hlapi.CommunityData(string))
                if poller_information:
                    for key, value in poller_information.items():
                        print("OID Description - {} :: OID {} :: Value - {}".format(description, oid, value))
                        poller_data[description] = value
            """
            SNMP WALK
            """
            for description, oid in poller_library['walk'].items():
                items = []
                items_dict = {}
                for (errorIndication,
                     errorStatus,
                     errorIndex,
                     varBinds) in nextCmd(SnmpEngine(),
                                          CommunityData(string),
                                          UdpTransportTarget((device_ip, 161)),
                                          ContextData(),
                                          ObjectType(ObjectIdentity(oid)),
                                          lookupMib=False,
                                          lexicographicMode=False):

                    if errorIndication:
                        print(errorIndication, file=sys.stderr)
                        break

                    elif errorStatus:
                        print('%s at %s' % (errorStatus.prettyPrint(),
                                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
                        break

                    else:
                        for varBind in varBinds:
                            """
                            Un hash the following line to see all the data that is being polled
                            """
                            #print("OID Description - {} :: OID Prefix - {} :: OID {} :: Value - {}".format(description, oid, list(varBind)[0], list(varBind)[1]))
                            oid = cast(list(varBind)[0])
                            oid_value = cast(list(varBind)[1])
                            dict = {}
                            dict = {oid: oid_value}
                            items_dict.update(dict)
                        poller_data[description] = items_dict

            """
            Return all the data that was found or save to the database depending on the flag
            """



            if regex_check_qfx:
                print("Saving poller data to database")
                try:

                    '''
                    Check if a backup exists. 
                    If it does, Update the row
                    If none exists, create a new entry
                    '''
                    with connect(
                            host=MY_DB_WRITE_CREDS.hostname,
                            user=MY_DB_WRITE_CREDS.username,
                            password=MY_DB_WRITE_CREDS.password,
                            database=MY_DB_WRITE_CREDS.database
                    ) as connection:
                        poller_data = json.dumps(poller_data)
                        cursor = connection.cursor()
                        """
                        poller_qfx_51xx_information is the table used to store the information for any qfx device. 
                        This table can be changed to suit your needs. This could be changed to a file / different table 
                        depending on your needs. Sending to an encrypted file may be a better choice if you are worried 
                        about the data being openly readable.
                        """
                        check_sql = """SELECT id FROM `poller_qfx_51xx_information` WHERE device_ip = %s"""
                        cursor.execute(check_sql, (device_ip,))
                        results = cursor.fetchall()
                        """
                        The calculated hash value is used to determine if the core information has changed. 
                        If not then the main program will not waste time processing the core data pulled from the poller.
                        """
                        calculated_md5 = hashlib.md5(poller_data.encode())
                        calculated_md5 = calculated_md5.hexdigest()

                        if cursor.rowcount >= 1:
                            cursor = connection.cursor()
                            delete_sql = """DELETE FROM poller_qfx_51xx_information WHERE device_ip = %s"""
                            cursor.execute(delete_sql, (device_ip,))
                            connection.commit()

                            """
                            Once the old entry is removed add the new one.
                            """
                            cursor = connection.cursor()
                            cursor.execute("""
                                                                           INSERT INTO poller_qfx_51xx_information 
                                                                           (device_ip, device_tid, device_type, information, md5, datetime)
                                                                           VALUES
                                                                           (%s,%s,%s,%s,%s,%s)
                                                                           """,
                                           (device_ip, device_tid, device_type_save, poller_data, calculated_md5, time.strftime('%Y-%m-%d %H:%M:%S')))
                            connection.commit()
                            connection.close()
                        else:
                            cursor = connection.cursor()
                            cursor.execute("""
                                                                           INSERT INTO poller_qfx_51xx_information 
                                                                           (device_ip, device_tid, device_type, information, md5, datetime)
                                                                           VALUES
                                                                           (%s,%s,%s,%s,%s,%s)
                                                                           """,
                                           (device_ip, device_tid, device_type_save, poller_data, calculated_md5, time.strftime('%Y-%m-%d %H:%M:%S')))
                            connection.commit()
                            connection.close()
                except TypeError as e:
                    print(e)
                sys.stdout.write(poller_data)
                sys.stdout.flush()
                sys.exit(0)
            else:
                notification("No library built for the device you are trying to poll, Or there has been an error in polling.")
else:
    notification("No device IP supplied")



