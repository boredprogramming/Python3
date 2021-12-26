import yaml
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader

def return_chassis_system_alarms(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            output = {}
            globals().update(FactoryLoader().load(yaml.load(table_view, Loader=yaml.FullLoader)))
            alarms = ShowChassisAlarms(dev)
            alarms.get()
            count = 0
            for item in alarms:
                output[count] = item
            return output
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)