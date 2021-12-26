"""
Juniper QFX
Retrieve interface diagnostics optics information and save to the database

"""


"""
Generic includes
"""
import os
import re
import json
import yaml
import sys
import json
import argparse
import socket
import time




"""
REGEX Checks
"""

fpc_regex = r'FPC\s([0-9]+)'
fpc_regex = re.compile(fpc_regex)

pic_regex = r'PIC\s([0-9]+)'
pic_regex = re.compile(pic_regex)

xcvr_regex = r'Xcvr\s([0-9]+)'
xcvr_regex = re.compile(xcvr_regex)

qfx_regex = r'.*(qfx5100-96s-8q|qfx5110-32q).*'
qfx_regex = re.compile(qfx_regex)

interface_regex = r'(([gxe][et]-)([0-9]{1,2}/){2}[0-9]{1,2})'
interface_regex = re.compile(interface_regex)

interface_fpc_pic_port_regex = r'([0-9]+)/([0-9]+)/([0-9]+)'
interface_fpc_pic_port_regex = re.compile(interface_fpc_pic_port_regex)



from additional_directories import production_paths
'''
Append the system path with where the script will be ran, This may differ
from computer (data bed) to the deployed server.
'''
for path in production_paths:
    sys.path.append(path)

"""
Functions to retrieve data from a qfx
"""
from Python.Python3.Juniper.juniper_functions.qfx_51xx.return_interface_diagnostics_optics import *
from Python.Python3.Juniper.juniper_functions.qfx_51xx.return_chassis_sub_sub_modules_xcvr import *

"""
Read only account
"""
from Python.Python3.packages.credentials.ro_creds import MY_RO_CREDENTIALS

"""
Juniper QFX Related table view
-Custom table views
"""
from Python.Python3.Juniper.juniper_qfx_ort import juniper_qfx_tables
FPCChassisSubModulesPICInformation = juniper_qfx_tables.FPCChassisSubModulesPICInformation
interfaceDiagnosticsOptics = juniper_qfx_tables.interfaceDiagnosticsOptics

"""
I removed all my database query portions of code from this. 
you can modify this code to save the data whereever you want it to go. 

"""

"""
Beginning of SNMP related functions
"""

"""
SNMP includes
"""
from Python.Python3.packages.snmp_strings.snmp_community_strings import MY_COMMUNITY_STRINGS
from Python.Python3.packages.snmp_library.snmp_library_file import library
from pysnmp import hlapi
from pysnmp.hlapi import nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

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

"""
END of SNMP related functions
"""


"""
BEGINNING OF MAIN PROGRAM
"""
parser = argparse.ArgumentParser(description='Return all interface diagnostic information for a QFX51XX device')
parser.add_argument('-device', '--device', help='Device TID or IP')
parser.add_argument('-bypass_dns_check', '--bypass_dns_check', help='bypass DNS lookup check')

args                        = parser.parse_args()
device                      = args.device
bypass_dns_check                      = args.bypass_dns_check

if not bypass_dns_check:
    bypass_dns_check = "No"

ip_regex = r'^(([0-9]{1,3}\.){3}[0-9]{1,3})$'
ip_regex = re.compile(ip_regex)
ip_regex = ip_regex.search(device)

tid_regex = r'^(\w{11})$'
tid_regex = re.compile(tid_regex)
tid_regex = tid_regex.search(device)

proceed = False

if bypass_dns_check != "Yes":
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
else:
    proceed = True
    device_tid = 'Unknown TID'
    device_ip = device


if proceed or bypass_dns_check == "Yes":
    """
    Validate the device is a QFX
    If so proceed. 
    This will also verify the correct SNMP string is loaded on the box
    """
    if device_ip:
        poller_library = False
        for string in MY_COMMUNITY_STRINGS.community:
            '''
            Which ever string is allowed to poll, Set that as the string to use
            '''
            try:
                information = get(device_ip, ['.1.3.6.1.2.1.1.1.0'], hlapi.CommunityData(string))
                """
                Regex for any specific portions of the device type. 
                This helps when there may be different types of replies from the same gear with different
                versions and you can point them all to the same library if applicable
                """
                if information:
                    allowed_string = string
                    for key, value in information.items():
                        device_type = value
                        """
                        Un hash the following line to see what is returned from the OID .1.3.6.1.2.1.1.1.0 -> SNMPv2-MIB::sysDescr.0
                        """
                    break

            except:
                allowed_string = "None"

    device_data = qfx_regex.search(device_type)

    """
    If the device type is a qfx the proceed with the audit
    """
    if device_data:
        print("Querying device with the TID/DNS Entry of {} and management ip of {}".format(device_tid, device_ip))

        data = {}
        data['chassis_sub_sub_modules_xcvr'] = return_chassis_sub_sub_modules_xcvr(device_ip=device_ip,
                                                                                   user=MY_RO_CREDENTIALS.username,
                                                                                   password=MY_RO_CREDENTIALS.password,
                                                                                   table_view=FPCChassisSubModulesPICInformation,
                                                                                   fpc_regex=fpc_regex,
                                                                                   pic_regex=pic_regex,
                                                                                   xcvr_regex=xcvr_regex,
                                                                                   juniper_tables=juniper_qfx_tables)

        data['interface_diagnostics_optics'] = return_interface_diagnostics_optics(device_ip=device_ip,
                                                                                   user=MY_RO_CREDENTIALS.username,
                                                                                   password=MY_RO_CREDENTIALS.password,
                                                                                   table_view=interfaceDiagnosticsOptics)
        """
        Convert from dict to json without single quotes
        """
        data = json.dumps(data)
        data = json.loads(data)



        for key, value in data['interface_diagnostics_optics'].items():
            for key_two, value_two in value.items():
                """
                data that this is an interface we want to record
                GE- XE- ET- 
                All others can be ignored
                """
                if key_two == 'interface':
                    s = interface_regex.search(value_two)
                    """
                    Search the chassis_sub_sub_modules_xcvr
                    for the wavelength value
                    """
                    breaker = False
                    for key_wave, value_wave in data['chassis_sub_sub_modules_xcvr'].items():
                        for key_two_wave, value_two_wave in data['chassis_sub_sub_modules_xcvr'][key_wave].items():
                            port_detail = interface_fpc_pic_port_regex.search(s[1])
                            if port_detail:
                                if data['chassis_sub_sub_modules_xcvr'][key_wave]['FPC'] == ("FPC " + port_detail[1]) \
                                        and data['chassis_sub_sub_modules_xcvr'][key_wave]['PIC'] == (
                                        "PIC " + port_detail[2]) \
                                        and data['chassis_sub_sub_modules_xcvr'][key_wave]['XCVR'] == (
                                        "Xcvr " + port_detail[3]):
                                    wave_length = data['chassis_sub_sub_modules_xcvr'][key_wave]['WAVELENGTH']
                                    breaker = True
                                    break
                            else:
                                wave_length = "Unknown"
                        if breaker:
                            break

                    if s[1]:
                        if s[2] == "ge-" or s[2] == "xe-":
                            """
                            Process the normal interface RX / TX values
                            """
                            DeviceClli = device_tid
                            DeviceIP = device_ip
                            interface = s[2] + port_detail[1] + "/" + port_detail[2] + "/" + port_detail[3]

                            interface_tx_dbm = data['interface_diagnostics_optics'][key]['laser_output_power_dbm']
                            if interface_tx_dbm == '- Inf':
                                interface_tx_dbm = 0

                            interface_rx_dbm = data['interface_diagnostics_optics'][key][
                                'rx_signal_avg_optical_power_dbm']
                            if interface_rx_dbm == '- Inf':
                                interface_rx_dbm = '-40'

                        elif s[2] == "et-":
                            """
                            Process the lanes optical values
                            """
                            DeviceClli = device_tid
                            DeviceIP = device_ip
                            interface = s[2] + port_detail[1] + "/" + port_detail[2] + "/" + port_detail[3]

                            interface_lane_index = data['interface_diagnostics_optics'][key]['lane_index']
                            if interface_lane_index == 'None':
                                interface_lane_index = ''

                            laser_output_power_dbm_lanes = data['interface_diagnostics_optics'][key][
                                'laser_output_power_dbm_lanes']
                            if laser_output_power_dbm_lanes == 'None':
                                laser_output_power_dbm_lanes = ''

                            laser_rx_optical_power_dbm_lanes = data['interface_diagnostics_optics'][key][
                                'laser_rx_optical_power_dbm_lanes']
                            if laser_rx_optical_power_dbm_lanes == 'None':
                                laser_rx_optical_power_dbm_lanes = ''



        
        
        
        
