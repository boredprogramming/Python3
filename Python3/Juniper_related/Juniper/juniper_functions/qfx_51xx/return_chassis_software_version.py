import yaml
import re
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader

"""
Software regex - Input will be item.name = junos -> comment
software_regex are the packages i want this to search
version_regex will be the version in between the []

This can be changed to suit your needs, 
I have not expanded on the software check portion of this yet so it it only 
pulling certain values. 

"""
software_regex = r'(JUNOS Base OS boot \[.*\]|JUNOS Base OS Software Suite \[.*\]|JUNOS Crypto Software Suite \[.*\]|JUNOS Online Documentation \[.*\]|JUNOS Kernel Software Suite \[.*\]|JUNOS Packet Forwarding Engine Support \[.*\])'
software_regex = re.compile(software_regex)

version_regex = r'\[(.*)\]'
version_regex = re.compile(version_regex)

def return_chassis_software_version(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            output = {}
            count = 0
            pass_fail = []
            globals().update(FactoryLoader().load(yaml.load(table_view, Loader=yaml.FullLoader)))
            software = ShowSoftwareVersion(dev)
            software.get()
            for item in software:
                output[count] = {'name': item.name, 'comment': item.comment}
                for sw in item.comment:
                    software_test = software_regex.search(sw)
                    if software_test:
                        version_search = version_regex.search(software_test[1])
                        if version_search:
                            if version_search[1] == kwargs['approved_software_values']['approved_software_revision']:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("###FAILED SOFTWARE VERSION CHECK###")
                    else:
                        pass_fail.append("Not checked in this revision")

                output[count]['pass_fail_status'] = pass_fail
                pass_fail = []
                count += 1

            return output
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)