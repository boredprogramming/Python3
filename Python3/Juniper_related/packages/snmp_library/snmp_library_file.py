def library(device_type):
    if device_type == "FSP150CC-GE114":
        library = {
            'get': {
                'device_tid': '.1.3.6.1.2.1.1.5.0',
                'device_type': '.1.3.6.1.2.1.1.1.0',
                'system_location': '.1.3.6.1.2.1.1.6.0',
                'snmp_engine_id': '1.3.6.1.6.3.10.2.1.1.0',
                'chassis_serial_number': '.1.3.6.1.2.1.47.1.1.1.1.11.1',
                'chassis_part_number': '.1.3.6.1.4.1.2544.1.12.3.1.3.1.8.1.1.1',
                'active_software_version': '.1.3.6.1.4.1.2544.1.12.3.1.3.1.10.1.1.1',
                'standby_software_version': '.1.3.6.1.4.1.2544.1.12.2.1.7.4.1.3.2',
                'download_software_version': '.1.3.6.1.4.1.2544.1.12.2.1.7.4.1.3.3',
            },
            'walk': {
                'interface_name': '.1.3.6.1.2.1.31.1.1.1.1',
                'interface_index': '.1.3.6.1.2.1.2.2.1.1',
                'network_port_interface_index_id': '.1.3.6.1.4.1.2544.1.12.4.1.7.1.2',
                'access_port_interface_index_id': '.1.3.6.1.4.1.2544.1.12.4.1.1.1.2',
                'interface_alias': '.1.3.6.1.2.1.31.1.1.1.18',
                'interface_admin_status': '.1.3.6.1.2.1.2.2.1.7',
                'interface_oper_status': '.1.3.6.1.2.1.2.2.1.8',
                'interface_crc_alignment_errors': '.1.3.6.1.2.1.16.1.1.1.8',

                'network_interface_sfp_vendor_name': '.1.3.6.1.4.1.2544.1.12.4.1.7.1.13',
                'network_interface_sfp_wave_length': '.1.3.6.1.4.1.2544.1.12.4.1.7.1.70',               #This object provides the SFP Laser Wave Length in nano meters. This is applicable only when cmEthernetNetPortMediaType is fiber.
                'network_interface_sfp_part_number': '.1.3.6.1.4.1.2544.1.12.4.1.7.1.14',
                'network_interface_optical_rx_value_dbm': '.1.3.6.1.4.1.2544.1.12.5.1.5.1.34',         # neIndex, shelfIndex, slotIndex, cmEthernetAccPortIndex, cmEthernetAccPortStatsIndex
                'network_interface_optical_tx_value_dbm': '.1.3.6.1.4.1.2544.1.12.5.1.5.1.33',         # neIndex, shelfIndex, slotIndex, cmEthernetAccPortIndex, cmEthernetAccPortStatsIndex

                'access_interface_sfp_vendor_name': '.1.3.6.1.4.1.2544.1.12.4.1.1.1.13',
                'access_interface_sfp_wave_length': '.1.3.6.1.4.1.2544.1.12.4.1.1.1.72',               # This object provides the SFP Laser Wave Length in nano meters. This is applicable only when cmEthernetNetPortMediaType is fiber.
                'access_interface_sfp_part_number': '.1.3.6.1.4.1.2544.1.12.4.1.1.1.14',
                'access_interface_optical_rx_value_dbm': '.1.3.6.1.4.1.2544.1.12.5.1.1.1.34',          # neIndex, shelfIndex, slotIndex, cmEthernetAccPortIndex, cmEthernetAccPortStatsIndex
                'access_interface_optical_tx_value_dbm': '.1.3.6.1.4.1.2544.1.12.5.1.1.1.33',          # neIndex, shelfIndex, slotIndex, cmEthernetAccPortIndex, cmEthernetAccPortStatsIndex


                'network_port_stats_average_bitrate_N2A_direction': '.1.3.6.1.4.1.2544.1.12.5.1.5.1.37', # neIndex, shelfIndex, slotIndex, cmEthernetNetPortIndex, cmEthernetNetPortStatsIndex
                'network_port_stats_average_bitrate_A2N_direction': '.1.3.6.1.4.1.2544.1.12.5.1.5.1.38', # neIndex, shelfIndex, slotIndex, cmEthernetNetPortIndex, cmEthernetNetPortStatsIndex
                                                                                                         # An arbitrary integer index value used to uniquely identify
                                                                                                         #    this Ethernet Network Port statistics entry.
                                                                                                         #    1 - 15min
                                                                                                         #    2 - 1day
                                                                                                         #    3 - rollover
                                                                                                         #    4 - 5min

                'access_port_stats_average_bitrate_N2A_direction': '.1.3.6.1.4.1.2544.1.12.5.1.1.1.38',  # Same as above
                'access_port_stats_average_bitrate_A2N_direction': '.1.3.6.1.4.1.2544.1.12.5.1.1.1.37',
            }
        }
    elif device_type == "FSP150CC-XG116PRO":
        library = {
            'get': {
                'device_tid': '.1.3.6.1.2.1.1.5.0',
                'device_type': '.1.3.6.1.2.1.1.1.0',
                'system_location': '.1.3.6.1.2.1.1.6.0',
                'snmp_engine_id': '1.3.6.1.6.3.10.2.1.1.0',
                'chassis_serial_number': '.1.3.6.1.2.1.47.1.1.1.1.11.1',
                'chassis_part_number': '.1.3.6.1.4.1.2544.1.12.3.1.3.1.8.1.1.1',
                'active_software_version': '.1.3.6.1.4.1.2544.1.12.3.1.3.1.10.1.1.1',
                'standby_software_version': '.1.3.6.1.4.1.2544.1.12.2.1.7.4.1.3.2',
                'download_software_version': '.1.3.6.1.4.1.2544.1.12.2.1.7.4.1.3.3',
            },
            'walk': {
                'interface_name': '.1.3.6.1.2.1.31.1.1.1.1',
                'interface_index': '.1.3.6.1.2.1.2.2.1.1',
                'network_port_interface_index_id': '.1.3.6.1.4.1.2544.1.12.4.1.7.1.2',
                'access_port_interface_index_id': '.1.3.6.1.4.1.2544.1.12.4.1.1.1.2',
                'interface_alias': '.1.3.6.1.2.1.31.1.1.1.18',
            }
        }
    elif device_type == "CIENA_SWITCH":
        library = {
            'get': {
                'device_tid': '.1.3.6.1.2.1.1.5.0',
                'device_type': '.1.3.6.1.2.1.1.1.0',
                'system_location': '.1.3.6.1.2.1.1.6.0',
                'snmp_engine_id': '1.3.6.1.6.3.10.2.1.1.0',
            },
            'walk': {
                'interface_name': '.1.3.6.1.2.1.31.1.1.1.1',
                'interface_index': '.1.3.6.1.2.1.2.2.1.1',
                'interface_alias': '.1.3.6.1.2.1.31.1.1.1.18',
                'interface_admin_state': '.1.3.6.1.2.1.2.2.1.7',
                'interface_oper_state': '.1.3.6.1.2.1.2.2.1.8',
            }
        }
    elif device_type == "QFX-51XX":
        library = {
            'get': {
                'device_tid': '.1.3.6.1.2.1.1.5.0',
                'device_type': '.1.3.6.1.2.1.1.1.0',
                'system_location': '.1.3.6.1.2.1.1.6.0',
                'snmp_engine_id': '1.3.6.1.6.3.10.2.1.1.0',
                'system_uptime_timeticks': '.1.3.6.1.2.1.1.3.0',
            },
            'walk': {
                'dot1dBasePortIfIndex': '.1.3.6.1.2.1.17.1.4.1.2', #The value of the instance of the ifIndex object, defined in IF-MIB, for the interface corresponding to this port
                'interface_index': '.1.3.6.1.2.1.2.2.1.1',
                'interface_name': '.1.3.6.1.2.1.2.2.1.2',
                'interface_alias': '.1.3.6.1.2.1.31.1.1.1.18',
                'interface_admin_state': '.1.3.6.1.2.1.2.2.1.7',
                'interface_oper_state': '.1.3.6.1.2.1.2.2.1.8',
                #'etherStatsCRCAlignErrors': '1.3.6.1.2.1.16.1.1.1.8',
                #'etherStatsCollisions': '1.3.6.1.2.1.16.1.1.1.13', # The best estimate of the total number of collisions on this Ethernet segment.
                                                                   # The value returned will depend on the location of the RMON probe. Section 8.2.1.3 (10BASE-5) and section 10.3.1.3
                                                                   # (10BASE-2) of IEEE standard 802.3 states that a station must detect a collision, in the receive mode, if three or
                                                                   # more stations are transmitting simultaneously. A repeater port must detect a collision when two or more stations are
                                                                   # transmitting simultaneously. Thus a probe placed on a repeater port could record more collisions than a probe connected
                                                                   # to a station on the same segment would.
                                                                   # Probe location plays a much smaller role when considering 10BASE-T. 14.2.1.4 (10BASE-T) of IEEE standard 802.3 defines a collision
                                                                   # as the simultaneous presence of signals on the DO and RD circuits (transmitting and receiving at the same time). A 10BASE-T station
                                                                   # can only detect collisions when it is transmitting. Thus probes placed on a station and a repeater, should report the same number of collisions.
                                                                   # Note also that an RMON probe inside a repeater should ideally report collisions between the repeater and one or more other hosts (transmit collisions
                                                                   # as defined by IEEE 802.3k) plus receiver collisions observed on any coax segments to which the repeater is connected.
                #'etherStatsDropEvents': '1.3.6.1.2.1.16.1.1.1.3',
                'interface_last_state_change_timeticks': '.1.3.6.1.2.1.2.2.1.9',
                'jnxL2aldVlanName': '.1.3.6.1.4.1.2636.3.48.1.3.1.1.2',
                'dot1qVlanStaticName': '1.3.6.1.2.1.17.7.1.4.3.1.1', #Vlan name configured on the device + vlan id in string form
                'dot1qVlanStaticEgressPorts': '1.3.6.1.2.1.17.7.1.4.3.1.2', #Egress ports assigned to each vlan.
                'dot1qVlanStaticRowStatus': '.1.3.6.1.2.1.17.7.1.4.3.1.5', #Status of each vlan -> {active(1), notInService(2), notReady(3), createAndGo(4), createAndWait(5), destroy(6) }
                'jnxL2aldVlanFdbId': '1.3.6.1.4.1.2636.3.48.1.3.1.1.5', #Vlan forwarding database reference id. Ex output -> .1.3.6.1.4.1.2636.3.48.1.3.1.1.5.174 = Gauge32: 11403264
                'dot1qTpFdbPort': '1.3.6.1.2.1.17.7.1.2.2.1.2', # Either the value '0', or the port number of the port on which a frame having a source address equal to the value
                                                                # of the corresponding instance of dot1qTpFdbAddress has been seen. A value of '0'
                                                                # indicates that the port number has not been learned but that the device does have some
                                                                # forwarding/filtering information about this address (e.g., in the dot1qStaticUnicastTable). Implementors are encouraged to
                                                                # assign the port value to this object whenever it is learned, even for addresses for which the corresponding value of dot1qTpFdbStatus
                                                                # is not learned(3).
                                                                # Example call / Filter 1.3.6.1.2.1.17.7.1.2.2.1.2.jnxL2aldVlanFdbId => Will return interface ids and mac addresses
                                                                # The End will need to be converted from decimal to hex to obtain the mac address.
                'arp_table': '.1.3.6.1.2.1.4.22.1.2',
            }
        }
    elif device_type == "MX":
        library = {
            'get': {
                'device_tid': '.1.3.6.1.2.1.1.5.0',
                'device_type': '.1.3.6.1.2.1.1.1.0',
                'system_location': '.1.3.6.1.2.1.1.6.0',
                'snmp_engine_id': '1.3.6.1.6.3.10.2.1.1.0',
                'system_uptime_timeticks': '.1.3.6.1.2.1.1.3.0',
            },
            'walk': {
                'dot1dBasePortIfIndex': '.1.3.6.1.2.1.17.1.4.1.2', #The value of the instance of the ifIndex object, defined in IF-MIB, for the interface corresponding to this port
                'interface_index': '.1.3.6.1.2.1.2.2.1.1',
                'interface_name': '.1.3.6.1.2.1.2.2.1.2',
                'interface_alias': '.1.3.6.1.2.1.31.1.1.1.18',
                'interface_admin_state': '.1.3.6.1.2.1.2.2.1.7',
                'interface_oper_state': '.1.3.6.1.2.1.2.2.1.8',
                #'etherStatsCRCAlignErrors': '1.3.6.1.2.1.16.1.1.1.8',
                #'etherStatsCollisions': '1.3.6.1.2.1.16.1.1.1.13', # The best estimate of the total number of collisions on this Ethernet segment.
                                                                   # The value returned will depend on the location of the RMON probe. Section 8.2.1.3 (10BASE-5) and section 10.3.1.3
                                                                   # (10BASE-2) of IEEE standard 802.3 states that a station must detect a collision, in the receive mode, if three or
                                                                   # more stations are transmitting simultaneously. A repeater port must detect a collision when two or more stations are
                                                                   # transmitting simultaneously. Thus a probe placed on a repeater port could record more collisions than a probe connected
                                                                   # to a station on the same segment would.
                                                                   # Probe location plays a much smaller role when considering 10BASE-T. 14.2.1.4 (10BASE-T) of IEEE standard 802.3 defines a collision
                                                                   # as the simultaneous presence of signals on the DO and RD circuits (transmitting and receiving at the same time). A 10BASE-T station
                                                                   # can only detect collisions when it is transmitting. Thus probes placed on a station and a repeater, should report the same number of collisions.
                                                                   # Note also that an RMON probe inside a repeater should ideally report collisions between the repeater and one or more other hosts (transmit collisions
                                                                   # as defined by IEEE 802.3k) plus receiver collisions observed on any coax segments to which the repeater is connected.
                #'etherStatsDropEvents': '1.3.6.1.2.1.16.1.1.1.3',
                'interface_last_state_change_timeticks': '.1.3.6.1.2.1.2.2.1.9',
                'jnxL2aldVlanFdbId': '1.3.6.1.4.1.2636.3.48.1.3.1.1.5', #Vlan forwarding database reference id. Ex output -> .1.3.6.1.4.1.2636.3.48.1.3.1.1.5.174 = Gauge32: 11403264
                'dot1qTpFdbPort': '1.3.6.1.2.1.17.7.1.2.2.1.2', # Either the value '0', or the port number of the port on which a frame having a source address equal to the value
                                                                # of the corresponding instance of dot1qTpFdbAddress has been seen. A value of '0'
                                                                # indicates that the port number has not been learned but that the device does have some
                                                                # forwarding/filtering information about this address (e.g., in the dot1qStaticUnicastTable). Implementors are encouraged to
                                                                # assign the port value to this object whenever it is learned, even for addresses for which the corresponding value of dot1qTpFdbStatus
                                                                # is not learned(3).
                                                                # Example call / Filter 1.3.6.1.2.1.17.7.1.2.2.1.2.jnxL2aldVlanFdbId => Will return interface ids and mac addresses
                                                                # The End will need to be converted from decimal to hex to obtain the mac address.
                'arp_table': '.1.3.6.1.2.1.4.22.1.2',           # Depending on your needs you could blank this out if you are not interested in the layer 3 arp table
            }
        }
    else:
        library = False

    return library

if __name__ == "__main__":

    '''
    If you run this .py script on it's own, you can test
    the library data with various gets / prints etc. 
    '''
    lib = library("MX")
    for description, oid in lib['get'].items():
        print("Target Name -> {} :: OID -> {}".format(description, oid))

    for description, oid in lib['walk'].items():
        print("Target Name -> {} :: OID -> {}".format(description, oid))
