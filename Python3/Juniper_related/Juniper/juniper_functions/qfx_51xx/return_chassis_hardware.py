import yaml

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader

def return_chassis_hardware(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            output = {}
            count = 0
            globals().update(FactoryLoader().load(yaml.load(table_view, Loader=yaml.FullLoader)))
            hardware = FpcHwTable(dev)
            hardware.get()
            for item in hardware:
                output[count] = {'name': item.name, 'serial_number': item.sn, 'part_number': item.pn, 'part_description': item.desc, 'version': item.ver, 'model': item.model}
                count += 1
            return output
        except ConnectError as err:
            print("Cannot connect to device: {0}".format(err))
            sys.exit(1)