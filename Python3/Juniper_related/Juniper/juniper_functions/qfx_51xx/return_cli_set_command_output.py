"""
Import the custom qfx table views,
you could pass them via the kwargs if you wanted.
"""

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader



def return_cli_set_show_configuration(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            """
            INIT VALUES
            """
            output = []
            fetch = dev.cli("show configuration | display set", warning=False)

            fetch = fetch.split('\n')
            while ("" in fetch):
                fetch.remove("")
            output = fetch
            return output
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)