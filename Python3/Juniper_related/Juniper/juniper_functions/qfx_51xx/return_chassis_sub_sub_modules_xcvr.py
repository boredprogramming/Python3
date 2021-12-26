"""
Import the custom qfx table views,
you could pass them via the kwargs if you wanted.
"""
import yaml

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader


def return_chassis_sub_sub_modules_xcvr(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']
    fpc_regex = kwargs['fpc_regex']
    pic_regex = kwargs['pic_regex']
    xcvr_regex = kwargs['xcvr_regex']
    juniper_tables = kwargs['juniper_tables']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            """
            STORE AVAILABLE FPC PIC COMBOS 
            """
            availableFPCPIC = []
            total = 0
            count = 0
            data = {}
            data[count] = {}
            globals().update(FactoryLoader().load(yaml.load(table_view, Loader=yaml.FullLoader)))
            hardware = FPCChassisSubModulesPICInformation(dev)
            hardware.get()
            final_audit_data = {}
            for item in hardware:
                fpc_pic = ""
                fpc_pic = item.fpc + " " + item.pic
                for x in item.xcvr:

                    availableFPCPIC.append(fpc_pic)
                    fpc_regex_check = fpc_regex.search(item.fpc)
                    pic_regex_check = pic_regex.search(item.pic)
                    xcvr_regex_check = xcvr_regex.search(item.xcvr[count])

                    if fpc_regex_check and pic_regex_check and xcvr_regex_check:
                        interface = fpc_regex_check[1] + "/" + pic_regex_check[1] + "/" + xcvr_regex_check[1]
                    else:
                        interface = "Unable to parse interface"

                    """
                    Get PIC details
                    EG
                    <port>
                        <port-number>4</port-number>
                        <cable-type>GIGE 1000LH</cable-type>
                        <fiber-mode>SM</fiber-mode>
                        <sfp-vendor-name>OEM             </sfp-vendor-name>
                        <sfp-vendor-pno>SFP-CWDM-1470-JN</sfp-vendor-pno>
                        <wavelength>1470 nm</wavelength>
                        <sfp-vendor-fw-ver>0.0</sfp-vendor-fw-ver>
                        <sfp-jnpr-ver>REV 01</sfp-jnpr-ver>
                    </port>
                    """

                    final_audit_data[total] = {}
                    final_audit_data[total] = {'FPC': item.fpc,
                                               'PIC': item.pic,
                                               'XCVR': item.xcvr[count],
                                               'XCVR_PART_NUMBER': item.xcvr_part_number[count],
                                               'XCVR_SERIAL_NUMBER': item.xcvr_serial_number[count],
                                               'XCVR_DESCRIPTION': item.xcvr_description[count]}
                    total += 1
                    count += 1
                count = 0
            unique_list = []

            """
            Make sure the list of available FPC / PICs is unique to avoid
            querying the router multiple times for the same items
            """
            for x in availableFPCPIC:
                if x not in unique_list:
                    unique_list.append(x)

            count = 0
            for x in unique_list:
                """
                Get the FPC PIC Combo and grab the appropriate hardware information for each
                """
                fpc_regex_check = fpc_regex.search(x)
                pic_regex_check = pic_regex.search(x)
                if fpc_regex_check and pic_regex_check:
                    """
                    Call the regex function to search the string for just the fpc or pic number
                    input FPC # | PIC #
                    output #
                    """
                    fpc = fpc_regex_check[1]
                    pic = pic_regex_check[1]
                    custom_table = juniper_tables.FPCChassisSubModulesPICInformationDetail
                    globals().update(FactoryLoader().load(yaml.load(custom_table.format(fpc, pic), Loader=yaml.FullLoader)))
                    pic_details = FPCChassisSubModulesPICInformationDetail(dev)
                    pic_details.get()

                    for pInfo in pic_details:
                        fpc = "FPC " + str(pInfo.slot)
                        pic = "PIC " + str(pInfo.pic_slot)
                        for i in range(0, len(final_audit_data)):
                            counter = 0
                            """
                            Check if we're in the appropriate FPC
                            """
                            if 'FPC' in final_audit_data[i] and fpc == final_audit_data[i]['FPC']:
                                """
                                Search the appropriate FPCs for the appropriate XCVR line
                                """
                                for port in pInfo.port_number:
                                    target_xcvr = "Xcvr " + port
                                    if 'FPC' in final_audit_data[i] and fpc == final_audit_data[i]['FPC'] and pic == final_audit_data[i]['PIC'] and target_xcvr == final_audit_data[i]['XCVR']:
                                        final_audit_data[i]['CABLE_TYPE'] = pInfo.cable_type[counter]
                                        final_audit_data[i]['FIBER_MODE'] = pInfo.fiber_mode[counter]
                                        final_audit_data[i]['WAVELENGTH'] = pInfo.wavelength[counter]
                                    counter += 1

            return final_audit_data
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)