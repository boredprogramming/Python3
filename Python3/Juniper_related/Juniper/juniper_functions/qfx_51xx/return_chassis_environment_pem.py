import yaml
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader

def return_chassis_environment_pem(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            """
            This is set to only pull the PEM status using the "member 0" argument. 
            As it shows ALL the pems in a virtual stack as well as all the ones in a single stack, 
            so it will account for multiple stacks / pems in 1 show.
            """
            output = {}
            count = 0
            globals().update(FactoryLoader().load(yaml.load(table_view.format("0"), Loader=yaml.FullLoader)))
            pem = ChassisEnvironmentPEM(dev)
            pem.get()
            for item in pem:
                if item.state == 'Online':
                    passfail = 'PASS'
                else:
                    """
                    If the pem status is not online, "No power" it will flag the status as 
                    failed.
                    """
                    passfail = '##FAIL##'
                output[count] = {'name': item.name, 'state': item.state, 'pass_fail_state': passfail}
                count += 1
            return output
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)