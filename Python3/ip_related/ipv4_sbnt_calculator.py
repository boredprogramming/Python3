"""
Take an input,
Either x.x.x.x/y (ip/cidr) or xxx.xxx.xxx.xxx (IP) yyy.yyy.yyy.yyy (subnet) format
Return all the ip addresses (network [first ip] and broadcast [last ip] as well)
"""
import logging
import sys
import re
import json
import ipaddress
import argparse

parser = argparse.ArgumentParser(description='Submit an IP / (CIDR/Subnet) mask to return all ips in a scope. Input can be "x.x.x.x/yy" or "1.1.1.1 255.255.255.0" or "1.1.1.1/255.255.255.0"')
parser.add_argument('-ip', '--ip', help='"IP/CIDR" - "IP MASK" - "IP/MASK"')
args = parser.parse_args()
ip = args.ip

"""
Regex statements for various checks
"""
cidr_regex = r'^(([0-9]{0,3}\.){3}[0-9]{1,3}/[0-9]{1,2})$'
ip_notation_regex = r'^(([0-9]{0,3}\.){3}[0-9]{0,3})(\s|/)(([0-9]{0,3}\.){3}[0-9]{0,3})$'

def json_me(obj):
    obj = json.dumps(obj)
    return obj

def sbnt_calc_cidr(input):
    """
    Returned data will be returned as a JSON object
    """

    returned_data = {}

    """
    Error Code = "" by default. 
    Will be populated on error
    """

    error = ''
    split_regex = r'^((\d{1,3}\.){3}\d{1,3})/(\d{1,2})$'
    split = re.compile(split_regex)
    split = split.match(input)
    if split:
        ip = split[1]
        cidr = int(split[3])
        """
        Is CIDR in the appropriate range 1 - 32
        """
        if (cidr >= 1) and (cidr <= 32):
            try:
                ip_list = []
                for ip in ipaddress.IPv4Network(input, strict=False):
                    ip_list.append(str(ip))
                returned_data = {'error': 'no_error', 'ip_list': ip_list}
                print(json_me(returned_data))
            except:
                error = 'Error proccessing input'
                returned_data = {'error': error}
                print(json_me(returned_data))
        else:
            error = 'CIDR Must be between 1 and 32'
            returned_data = {'error': error}
            print(json_me(returned_data))
    else:
        return False

def sbnt_calc_ip_notation(input):
    """
    Convert the subnet mask to CIDR and call the sbnt_calc_cidr function
    """
    try:
        """
        Split input on space " " or slash "/"
        """
        i = re.split('\s|/', input)
        CIDR = ipaddress.IPv4Network(i[0] + '/' + i[1]).prefixlen
        sbnt_calc_cidr(i[0] + '/' + str(CIDR))
    except Exception as ex:
        error = str(ex)
        returned_data = {'error': error}
        print(json_me(returned_data))

def check(ip_input):
    """
    Check the format to see which category it falls under.
    Either CIDR / Subnet notation / Throw it the hell out
    """

    cidr_test = re.compile(cidr_regex)
    cidr_test = cidr_test.search(ip_input)

    ip_notation_test = re.compile(ip_notation_regex)
    ip_notation_test = ip_notation_test.search(ip_input)

    if cidr_test:
        sbnt_calc_cidr(ip_input)
    elif ip_notation_test:
        sbnt_calc_ip_notation(ip_input)
    else:
        returned_data = {'error': "Invalid Input"}
        print(json_me(returned_data))

if __name__ == '__main__':
    check(ip)