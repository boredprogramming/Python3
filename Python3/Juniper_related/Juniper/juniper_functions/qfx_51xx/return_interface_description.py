import json
import yaml
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader
from jnpr.junos.op.ethport import EthPortTable
import lxml

def return_interface_description(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            output = {}
            count = 0
            physical_interface = dev.rpc.get_interface_information()
            physical_interface_information = physical_interface.findall('.//physical-interface')

            for item in physical_interface_information:
                name = item.find('.//name').text
                admin_status = item.find('.//admin-status').text
                oper_status = item.find('.//oper-status').text
                mtu = item.find('.//mtu').text

                """
                Test to see if these exist in the xml output
                """
                test_description = item.find('.//description')
                test_link_level_type = item.find('.//link-level-type')

                if test_description is not None:
                    description = item.find('.//description').text
                else:
                    description = "No Description"

                if test_link_level_type is not None:
                    link_level_type = item.find('.//link-level-type').text
                else:
                    link_level_type = "No Link Level Type"

                output[count] = {'interface': name, 'admin_status': admin_status, 'oper_status': oper_status, 'description': description, 'mtu': mtu, 'link_level_type': link_level_type}
                count += 1
            return output
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)