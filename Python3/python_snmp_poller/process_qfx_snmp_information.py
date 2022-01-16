"""
This will take the information that is pulled from the SNMP walk of a QFX device
and saved into the database and process it so all the data is condensed and outputted
in some nice neat little json package that will make your parser happy. Maybe

Any data this is programmed to process is all apart of the snmp_library file and nothing else.
Any new data will need to be added if desired.
"""

import argparse
import json
import sys
import re
import socket

from additional_directories import production_paths
'''
Append the system path with where the script will be ran, This may differ
from computer (data bed) to the deployed server.
'''
for path in production_paths:
    sys.path.append(path)
import time
from datetime import datetime, timedelta
from Python.Python3.packages.credentials.ro_creds import MY_DB_READONLY_CREDS
from Python.Python3.packages.credentials.wr_creds import MY_DB_WRITE_CREDS
from mysql.connector import connect, Error

parser = argparse.ArgumentParser(description='Process and return snmp walk info from the QFX device scans from the '
                                             'poller_qfx_51xx_information database')
parser.add_argument('-device', '--device', help='Device TID or IP')

args        = parser.parse_args()
device        = args.device


def notification(data):
    data = data
    data = json.dumps(data)
    sys.stdout.write(data)
    sys.stdout.flush()
    sys.exit(0)





def decimalToHexadecimal(decimal):
    # Conversion table of remainders to
    # hexadecimal equivalent
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                        5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                        13: 'D', 14: 'E', 15: 'F'}

    hexadecimal = ''
    if decimal == 0:
        value = str(0).zfill(2)
        return value
    else:
        while (decimal > 0):
            remainder = decimal % 16
            hexadecimal = conversion_table[remainder] + hexadecimal
            decimal = decimal // 16
        return hexadecimal.zfill(2)

def processQFXData(device):
    if device:
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
                device_tid = False
                proceed = True
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
            if device_ip:
                try:
                    with connect(
                            host=MY_DB_READONLY_CREDS.hostname,
                            user=MY_DB_READONLY_CREDS.username,
                            password=MY_DB_READONLY_CREDS.password,
                            database=MY_DB_READONLY_CREDS.database
                    ) as connection:
                        cursor = connection.cursor(dictionary=True)
                        """
                        poller_qfx_51xx_information is the name of the table on the selected database where the snmp information is stored
                        and retrieved. This can be changed to suit your needs.
                        """
                        check_sql = """SELECT information FROM poller_qfx_51xx_information WHERE device_ip = %s"""
                        cursor.execute(check_sql, (device_ip,))
                        results = cursor.fetchone()
                        connection.close()
                        count = 0
                        interface_data = {}
                        if results:
                            """
                            Find all the interface snmp index ids
                            """
                            jsonObj = json.loads(results['information'])
                            for key, value in jsonObj['dot1dBasePortIfIndex'].items():
                                interface_data[count] = {}
                                """
                                Convert admin/oper state into up/down value
                                """
                                if jsonObj['interface_admin_state']['1.3.6.1.2.1.2.2.1.7.' + str(value)] == 1:
                                    admin_state = 'up'
                                elif jsonObj['interface_admin_state']['1.3.6.1.2.1.2.2.1.7.' + str(value)] == 2:
                                    admin_state = 'down'
                                else:
                                    admin_state = 'unknown'

                                if jsonObj['interface_oper_state']['1.3.6.1.2.1.2.2.1.8.' + str(value)] == 1:
                                    oper_state = 'up'
                                elif jsonObj['interface_oper_state']['1.3.6.1.2.1.2.2.1.8.' + str(value)] == 2:
                                    oper_state = 'down'
                                else:
                                    oper_state = 'unknown'


                                """
                                Calculate last state change based on timeticks
                                If this is run on windows, you may get ticks in milliseconds so seconds would = ticks/1000 and not ticks/100
                                """
                                ticks = int(jsonObj['system_uptime_timeticks'] - jsonObj['interface_last_state_change_timeticks']['1.3.6.1.2.1.2.2.1.9.' + str(value)])
                                seconds = ticks/100
                                interface_uptime = timedelta(seconds=seconds)

                                days = str(interface_uptime.days)
                                leftover = str(timedelta(seconds=interface_uptime.seconds))
                                leftover = leftover.split(":")
                                hours = str(leftover[0])

                                if int(hours) == 1:
                                    hours_label = hours + " hour,"
                                elif int(hours) > 1:
                                    hours_label = hours + " hours,"
                                elif int(hours) == 0:
                                    hours_label = ""

                                minutes = " " + str(leftover[0])
                                seconds = str(leftover[0])

                                interface_state_change_label = days + " days, " + hours_label + minutes + " minutes, " + seconds + " seconds"
                                interface_data[count] = {
                                    'snmp_interface_index': value,
                                    'interface_name': jsonObj['interface_name']['1.3.6.1.2.1.2.2.1.2.' + str(value)],
                                    'interface_alias': jsonObj['interface_alias']['1.3.6.1.2.1.31.1.1.1.18.' + str(value)],
                                    'interface_admin_state': admin_state,
                                    'interface_oper_state': oper_state,
                                    'interface_state_change': interface_state_change_label
                                    }
                                count += 1


                            """
                            Find all the vlans configured on the switch
                            """
                            vlans = {}
                            id_information = {}
                            count = 0
                            for key, value in jsonObj['dot1qVlanStaticName'].items():
                                v = value.split("+")
                                """
                                Find all the interfaces this vlan is a part of
                                """
                                egress_ports = jsonObj['dot1qVlanStaticEgressPorts']['1.3.6.1.2.1.17.7.1.4.3.1.2.' + str(v[1])]
                                split_at = ","
                                if split_at in str(egress_ports):
                                    dot1dBasePortIfIndex = egress_ports.split(",")
                                else:
                                    dot1dBasePortIfIndex = egress_ports

                                """
                                Grab the interface index id of the interface this vlan is allowed to egress
                                """
                                interfaces = []
                                interface_index_ids = []
                                if not isinstance(dot1dBasePortIfIndex, list):
                                    interfaces.append(jsonObj['interface_name']['1.3.6.1.2.1.2.2.1.2.' + str(
                                        jsonObj['dot1dBasePortIfIndex']['1.3.6.1.2.1.17.1.4.1.2.' + str(dot1dBasePortIfIndex)])])
                                    interface_index_ids.append(
                                        jsonObj['dot1dBasePortIfIndex']['1.3.6.1.2.1.17.1.4.1.2.' + str(dot1dBasePortIfIndex)])
                                else:
                                    for i in dot1dBasePortIfIndex:
                                        interfaces.append(jsonObj['interface_name']['1.3.6.1.2.1.2.2.1.2.' + str(
                                            jsonObj['dot1dBasePortIfIndex']['1.3.6.1.2.1.17.1.4.1.2.' + str(i)])])
                                        interface_index_ids.append(
                                            jsonObj['dot1dBasePortIfIndex']['1.3.6.1.2.1.17.1.4.1.2.' + str(i)])

                                """
                                Get the id values for each vlan
                                """
                                counter = 0
                                id_regex = r'1.3.6.1.4.1.2636.3.48.1.3.1.1.2.([0-9]+)$'
                                id_regex = re.compile(id_regex)

                                for keyjnxL2aldVlanName, valuejnxL2aldVlanName in jsonObj['jnxL2aldVlanName'].items():
                                    """
                                    key / id[0] = entire oid string
                                    value = vlan name
                                    id[1] = vlan id to cross reference with ports / mac addresses
                                    """

                                    id = id_regex.search(keyjnxL2aldVlanName)
                                    if id:
                                        """
                                        jnxL2aldVlanFdbId
                                        Grab the vlan fdb id
                                        """
                                        jnxL2aldVlanFdbId = jsonObj['jnxL2aldVlanFdbId']['1.3.6.1.4.1.2636.3.48.1.3.1.1.5.' + str(id[1])]
                                        id_information[counter] = {}
                                        id_information[counter] = {'vlan_name': valuejnxL2aldVlanName, 'vlan_index_id': id[1], 'jnxL2aldVlanFdbId': jnxL2aldVlanFdbId}

                                        counter += 1
                                    else:
                                        interface_index_ids = []


                                vlans[count] = {'vlan_name': v[0], 'vlan_id': v[1],
                                                'allowed_egress_interfaces': interfaces,
                                                'egress_interface_index_ids': interface_index_ids}

                                interfaces = []
                                count += 1


                            """
                            Combine the different data sources into one final value to return
                            """
                            final = {}
                            final['vlan_data'] = {}
                            count = 0
                            for k, v in vlans.items():
                                for k2, v2 in id_information.items():
                                    if v['vlan_name'] == v2['vlan_name']:
                                        v.update(v2)
                                        final['vlan_data'][count] = v
                                        count += 1

                            """
                            Convert jnxL2aldVlanFdbId to a list for searching
                            """

                            dot1qTpFdbPortList = []
                            for keyFdb, valueFdb in jsonObj['dot1qTpFdbPort'].items():
                                dot1qTpFdbPortList.append(keyFdb)

                            """
                            Find all MAC Address values and which interface they are found on
                            """

                            """
                            The following variable is used to keep track of the 
                            mac address -> ingress interface information 
                            This way it allows the user to keep track of the mac table in a separate database table. 
                            """
                            mac_address_to_ingress_interface = {}


                            count = 0
                            count_macs = 0
                            count_mac_to_interface = 0
                            for key, value in final['vlan_data'].items():

                                mac_address_information = {}
                                search = ['.' + str(value['jnxL2aldVlanFdbId']) + '.']
                                """
                                macs = List of mac addresses in snmp - decimal form. 
                                Use this value to get the port id and port name that has learned this mac address
                                """
                                macs = [s for s in dot1qTpFdbPortList if any(xs in s for xs in search)]
                                for m in macs:
                                    """
                                    Extract the decimal form of the mac address and convert it to hex
                                    """

                                    mac_regex = r'1.3.6.1.2.1.17.7.1.2.2.1.2.(' + str(value['jnxL2aldVlanFdbId']) + ')\.(([0-9]+\.){5}[0-9]+)$'
                                    mac_regex = re.compile(mac_regex)
                                    mac = mac_regex.search(m)
                                    if mac[2]:
                                        mac_address = mac[2].split('.')
                                        for i in range(len(mac_address)):
                                            mac_address[i] = decimalToHexadecimal(int(mac_address[i]))
                                        mac_address = ':'.join(mac_address)
                                    else:
                                        mac_address = "Unable to convert - Error"

                                    """
                                    Find the ingress interface the mac address has been found on
                                    """
                                    ingress_interface = ""
                                    ingress_interface = jsonObj['interface_name']['1.3.6.1.2.1.2.2.1.2.' + str((jsonObj['dot1dBasePortIfIndex']['1.3.6.1.2.1.17.1.4.1.2.' + str(jsonObj['dot1qTpFdbPort'][m])]))]

                                    """
                                    Save the final information and append it to the final output.
                                    """

                                    mac_address_information[count_macs] = {'mac_address_interface_index': jsonObj['dot1qTpFdbPort'][m], 'mac_address_decimal': m, 'mac_address_hexidecimal': mac_address, 'ingress_interface': ingress_interface}

                                    """
                                    Save the mac address information to a separate variable that only tacks ingress 
                                    interface -> mac address information
                                    """
                                    mac_address_to_ingress_interface[count_mac_to_interface] = {}
                                    mac_address_to_ingress_interface[count_mac_to_interface] = {'vlan_name': value['vlan_name'], 'vlan_id': value['vlan_id'], 'ingress_interface_index': jsonObj['dot1qTpFdbPort'][m], 'ingress_interface': ingress_interface, 'mac_address_hexidecimal': mac_address_information[count_macs]['mac_address_hexidecimal']}
                                    count_mac_to_interface += 1
                                    count_macs += 1


                                final['vlan_data'][count]['mac_address_information'] = mac_address_information
                                mac_address_information = {}
                                count += 1
                                count_macs = 0

                            """
                            Sort and assign the information into a single variable to return
                            """

                            final['interface_data'] = {}
                            final['interface_data'] = interface_data
                            final['system_information'] = {}
                            final['system_information']['device_tid'] = device_tid
                            final['system_information']['device_ip'] = device_ip
                            final['system_information']['device_type'] = jsonObj['device_type']
                            final['system_information']['system_location'] = jsonObj['system_location']

                            """
                            START Processing of data that will be saved to the server. 
                            """

                            """
                            Generate query for the router interface status table insert
                            """

                            """
                            Delete old entries
                            """
                            try:
                                with connect(
                                        host=MY_DB_WRITE_CREDS.hostname,
                                        user=MY_DB_WRITE_CREDS.username,
                                        password=MY_DB_WRITE_CREDS.password,
                                        database=MY_DB_WRITE_CREDS.database
                                ) as connection:
                                    cursor = connection.cursor()

                                    """
                                    Delete all current entries in the interface status table
                                    router_interface_status is the table name (Can be changed to suit your needs) where the 
                                    interface status and state change information is stored.
                                    """
                                    delete_sql = """DELETE FROM router_interface_status WHERE device_ip = %s"""
                                    cursor.execute(delete_sql, (device_ip,))
                                    connection.commit()

                                    """
                                    Delete all current entries in the mac address table
                                    """

                                    delete_sql = """DELETE FROM device_arp_mac_table WHERE device_ip = %s"""
                                    cursor.execute(delete_sql, (device_ip,))
                                    connection.commit()

                                    """
                                    Insert the new entries
                                    """
                                    insert = """
                                    INSERT INTO router_interface_status 
                                    (device_ip, interface, interface_description, interface_admin_status, interface_oper_status, interface_state_change, datetime)
                                    VALUES
                                    """

                                    for k, v in interface_data.items():
                                        values = "(\"" + device_ip + "\",\"" + v['interface_name'] + "\",\"" + v[
                                            'interface_alias'] + "\",\"" + v['interface_admin_state'] + "\",\"" + v[
                                                     'interface_oper_state'] + "\",\"" + v[
                                                     'interface_state_change'] + "\",\"" + time.strftime(
                                            '%Y-%m-%d %H:%M:%S') + "\"),"
                                        insert += values
                                    try:
                                        cursor = connection.cursor()
                                        cursor.execute(insert[:-1])
                                        connection.commit()
                                    except TypeError as e:
                                        print(e)
                                    """
                                    Insert the new entries into the table tracking the mac address -> interface information
                                    device_arp_mac_table is the table name storing the mac address -> interface information. 
                                    Can be changed to suit your needs.
                                    """
                                    insert = """
                                             INSERT INTO device_arp_mac_table 
                                             (device_ip, ip, mac_address, interface_index, interface, datetime)
                                             VALUES
                                             """
                                    for k, v in mac_address_to_ingress_interface.items():
                                        ip = '' # This is blank until i program in a cross reference to find the associated arp either via the upstream
                                                # mx or ip arp on the qfx. This really depends on your usage of the QFX and whether it is a strict
                                                # layer 2 switch with an aggregation router that is doing all the routing etc, or if the qfx itself is doing
                                                # the routing and whether it will have a larger arp table that you may be interested in.
                                        ingress_interface = v['ingress_interface'] + ":" + v['vlan_name'] + ":VlanID:" + v['vlan_id']
                                        values = "(\"" + device_ip + "\",\"" + ip + "\",\"" + str(
                                            v['mac_address_hexidecimal']) + "\",\"" + str(v['ingress_interface_index']) + "\",\"" + ingress_interface + "\",\"" + time.strftime(
                                            '%Y-%m-%d %H:%M:%S') + "\"),"
                                        insert += values
                                    try:
                                        cursor = connection.cursor()
                                        cursor.execute(insert[:-1])
                                        connection.commit()
                                    except TypeError as e:
                                        print(e)

                                    connection.close()

                            except TypeError as e:
                                    print(e)

                            """
                            Process the mac table information in order to save it into the database
                            """

                            """
                            END Processing of data that will be saved to the server. 
                            """
                            notification(final)
                except TypeError as e:
                    print(e)

if __name__ == "__main__":
    processQFXData(device)