import yaml
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader



def return_chassis_virtual_chassis_information(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            """
            There are at a max 2 chassis in a stack. 
            This will prevent duplicates from being shown due to the xml output.
            """
            output = {}
            count = 0
            globals().update(FactoryLoader().load(yaml.load(table_view, Loader=yaml.FullLoader)))
            virtual = ShowVirtualChassis(dev)
            virtual.get()
            for item in virtual:
                if item.member_status == 'Prsnt':
                    success = 'PASS'
                else:
                    success = '###FAIL###'
                output[count] = {'member_id': item.member_id, 'member_status': item.member_status, 'fpc_slot': item.fpc_slot, 'serial_number': item.member_serial_number, 'model_number': item.member_model, 'member_priority': item.member_priority, 'member_role': item.member_role, 'pass_fail_status': success}
                count += 1
            return output
        except ConnectError as err:
            print("Cannot connect to device: {0}".format(err))
            sys.exit(1)