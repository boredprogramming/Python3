"""
Import the custom qfx table views,
you could pass them via the kwargs if you wanted.
"""
import json
import re
import time
import yaml
"""
REGEX Checks
"""

fpc_regex = r'FPC\s([0-9]+)'
fpc_regex = re.compile(fpc_regex)

pic_regex = r'PIC\s([0-9]+)'
pic_regex = re.compile(pic_regex)

xcvr_regex = r'Xcvr\s([0-9]+)'
xcvr_regex = re.compile(xcvr_regex)

mx_regex = r'.*(mx960|mx480|mx240).*'
mx_regex = re.compile(mx_regex)

interface_regex = r'(([gxe][et]-)([0-9]{1,2}/){2}[0-9]{1,2})'
interface_regex = re.compile(interface_regex)

interface_fpc_pic_port_regex = r'([0-9]+)/([0-9]+)/([0-9]+)'
interface_fpc_pic_port_regex = re.compile(interface_fpc_pic_port_regex)



from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader
from Python.Python3.Juniper.juniper_functions.mx_960_480_240.return_interface_diagnostics_optics import *

"""
Create and import your own credentials here to use with whatever connections you have
"""
from Python.Python3.packages.credentials.wr_creds import some_cred_variable
from mysql.connector import connect, Error

def returnChassisInfo(**kwargs):

    device_tid = kwargs['device_tid']
    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    fpc_regex = kwargs['fpc_regex']
    pic_regex = kwargs['pic_regex']
    juniper_tables = kwargs['juniper_tables']


    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:

            """
            INIT Variables
            """
            optics = {}
            count = 0
            data = {}

            """
            You can init an sql entry here if you are storing the data directly from this program into a monitoring database
            or however you would like to do it. 
            
            Then below during each cycle through the GE/XE/ET interface section just append to the string.
            """
            insert = """
            INSERT INTO somewhere
            """

            """
            Assign the table view
            """

            table = juniper_tables.returnChassisFPCPICList.format("FPC")
            globals().update(FactoryLoader().load(yaml.load(table, Loader=yaml.FullLoader)))
            pics = returnChassisFPCPICList(dev)
            pics.get()
            for p in pics:
                data[count] = {}
                data[count] = {p.fpc: p.pic}
                count += 1

            data = json.dumps(data)
            data = json.loads(data)
            count = 0
            for key, value in data.items():
                for fpc, pics in value.items():
                    for i in pics:
                        f = fpc_regex.search(fpc)
                        p = pic_regex.search(i)
                        table = juniper_tables.FPCChassisSubModulesPICInformationDetail.format(f[1], p[1])
                        globals().update(FactoryLoader().load(yaml.load(table, Loader=yaml.FullLoader)))
                        xcvr = FPCChassisSubModulesPICInformationDetail(dev)
                        xcvr.get()
                        if xcvr:

                            for x in xcvr:
                                item_count = 0
                                optics[count] = {}

                                """
                                Clear the values each run
                                """
                                port_number = []
                                cable_type = []
                                fiber_mode = []
                                wavelength = []
                                if len(x.port_number) <= 1:
                                    """
                                    Prevent issues when there is only 1 result in the list as trying to reference
                                    a list of 1 with a counter variable returns the first character generally.
                                    """
                                    port_number = x.port_number
                                    cable_type = x.cable_type
                                    fiber_mode = x.fiber_mode
                                    wavelength = x.wavelength
                                else:
                                    port_number = x.port_number[item_count]
                                    cable_type = x.cable_type[item_count]
                                    fiber_mode = x.fiber_mode[item_count]
                                    wavelength = x.wavelength[item_count]


                                for f in x.port_number:
                                    optics[count] = {'FPC': x.slot, 'PIC': x.pic_slot, 'PORT': port_number, 'CABLE_TYPE': cable_type, 'FIBER_MODE': fiber_mode, 'WAVELENGTH': wavelength}
                                    item_count += 1
                                    count += 1


            """
            Get the interface diagnostics optics information for every port
            """
            table = juniper_tables.interfaceDiagnosticsOptics
            diagnostics_optics = return_interface_diagnostics_optics(device_ip=device_ip,
                                                                                       user=username,
                                                                                       password=password,
                                                                                       table_view=table)


            for key, value in diagnostics_optics.items():
                for key_two, value_two in value.items():
                    """
                    data that this is an interface we want to record
                    GE- XE- ET- 
                    All others can be ignored for now. 
                    """
                    if key_two == 'interface':
                        s = interface_regex.search(value_two)
                        """
                        Search the chassis_sub_sub_modules_xcvr
                        for the wavelength value
                        """
                        breaker = False
                        for key_wave, value_wave in optics.items():
                            for key_two_wave, value_two_wave in optics[key_wave].items():
                                port_detail = interface_fpc_pic_port_regex.search(s[1])
                                if port_detail:
                                    if optics[key_wave]['FPC'] == (port_detail[1]) and optics[key_wave]['PIC'] == (
                                    port_detail[2]) and optics[key_wave]['PORT'] == (port_detail[3]):
                                        wave_length = optics[key_wave]['WAVELENGTH']
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
                                interface_tx_dbm = diagnostics_optics[key]['laser_output_power_dbm']
                                if interface_tx_dbm == '- Inf':
                                    interface_tx_dbm = 0

                                interface_rx_dbm = diagnostics_optics[key][
                                    'rx_signal_avg_optical_power_dbm']
                                if interface_rx_dbm == '- Inf':
                                    """
                                    - Inf = no light, -40 is close enough to 0 in laser world.
                                    """
                                    interface_rx_dbm = '-40'

                                """
                                This will generate the insert query for the database that is being used
                                to track light levels. Adjust as needed for your own.
                                """

                                """
                                Add your own data formatting here. 
                                This was being used to generate an insert query to save the data into a database.
                                For this file, it's currently excluded.
                                """
                            elif s[2] == "et-":
                                """
                                Process the lanes optical values
                                """
                                DeviceClli = device_tid
                                DeviceIP = device_ip
                                interface = s[2] + port_detail[1] + "/" + port_detail[2] + "/" + port_detail[3]

                                interface_lane_index = diagnostics_optics[key]['lane_index']
                                if interface_lane_index == 'None':
                                    interface_lane_index = ''

                                laser_output_power_dbm_lanes = diagnostics_optics[key][
                                    'laser_output_power_dbm_lanes']
                                if laser_output_power_dbm_lanes == 'None':
                                    laser_output_power_dbm_lanes = ''

                                laser_rx_optical_power_dbm_lanes = diagnostics_optics[key][
                                    'laser_rx_optical_power_dbm_lanes']
                                if laser_rx_optical_power_dbm_lanes == 'None':
                                    laser_rx_optical_power_dbm_lanes = ''

                                """
                                This will generate the inser query for the database that is being used
                                to track light levels. Adjust as needed for your own.
                                """
                                """
                                Add your own data formatting here. 
                                This was being used to generate an insert query to save the data into a database.
                                For this file, it's currently excluded.
                                """
            """
            Connect and add the entry to the database being used for tracking.
            Pass credentials from the cred library
            
            Some fancy database code below of your choosing.
            """


