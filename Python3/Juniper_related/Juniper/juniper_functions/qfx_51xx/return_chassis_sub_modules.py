import yaml
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader

def return_chassis_sub_modules(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            status = {}
            globals().update(FactoryLoader().load(yaml.load(table_view, Loader=yaml.FullLoader)))
            hardware = FPCChassisSubModules(dev)
            hardware.get()
            counter = 0
            for item in hardware:
                status[counter] = {}
                status[counter] = {'name': item.name, 'part_number': item.pn, 'serial_number': item.sn, 'description': item.description, 'clei_code': item.clei_code, 'model_number': item.model_number}
                counter += 1
            return status
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)