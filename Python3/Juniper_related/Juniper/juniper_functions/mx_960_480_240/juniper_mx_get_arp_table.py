"""
Incomplete, was just experimenting with the PyEZ calls
"""

"""
BEGINNING OF YML VARIABLES
"""
ArpTable = """
---
ArpTable:
  rpc: get-arp-table-information
  args:
    no-resolve: True
  item: arp-table-entry
  key: mac-address
  view: ArpView

ArpView:
  fields:
    mac_address: mac-address
    ip_address: ip-address
    interface_name: interface-name
"""

"""
END OF YML VARIABLES
"""


"""
Retrieve and process the layer 3 arp table
of a juniper MX Device.
"""
from additional_directories import production_paths
import os
import yaml
import sys
import json
import argparse
'''
Append the system path with where the script will be ran, This may differ
from computer (Test bed) to the deployed server.
'''
for path in production_paths:
    sys.path.append(path)

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml
from Python.Python3.packages.credentials.ro_creds import MY_RO_CREDENTIALS

parser = argparse.ArgumentParser(description='Log into juniper mx device and get the layer3 arp table')
parser.add_argument('-device_ip', '--device_ip', help='Device management IP')

args                        = parser.parse_args()
device_ip                   = args.device_ip

"""
START OF FUNCTIONS
"""
def return_arp(device, data_type):
    with Device(host=device, user=MY_RO_CREDENTIALS.username, password=MY_RO_CREDENTIALS.password, gather_facts=False, normalize=True) as dev:
        globals().update(FactoryLoader().load(yaml.load(ArpTable, Loader=yaml.FullLoader)))
        arp = ArpTable(dev)
        arp.get()
        for p in arp:
            print("{} {} {}".format(p.mac_address, p.ip_address, p.interface_name))


print("Connecting to {}".format(device_ip))
return_arp(device_ip, 'JSON')








