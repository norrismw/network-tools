#!/usr/bin/python3
# AntiAmericanJobs.py
# Author: Michael Norris
# GitHub: https://github.com/norrismw/

import sys
import re
import csv
import getpass
from netmiko import ConnectHandler

## used regardless of choice; used in gen_commands(), status_list(), and get_count()
# generates list of policies
def get_policies():
    policy_string = net_connect.send_command('show firewall policy | grep edit')
    policy_list = [int(s) for s in policy_string.split() if s.isdigit()]
    policy_list.append(0)
    return policy_list


## used regardless of choice; used in clear_count() and messy_hits()
# generates list of commands based on choice of show/clear and list of policies
def gen_commands():
    gen_commands = []
    for policy_id in get_policies():
        gen_commands.append(base_command + ' ' + str(policy_id))
    return gen_commands


## used if choice == "clear"
# sends the list of generated clear commands
def clear_count():
    print('[!] Clearing hit counts ...')
    for command in gen_commands():
        net_connect.send_command(command)
    return 0


## used if choice == "count"; used in clean_hits()
# generates messy hit count list from output of show commands; used in clean_hits()
def messy_hits():
    messy_hits = []
    for command in gen_commands():
        messy_hits.append(net_connect.send_command(command))
    return messy_hits


## used if choice == "count"
# cleans messy_hits list; used in get_count()
def clean_hits():
    clean_hits = []
    for command_output in messy_hits():
        hits_true = re.findall(r'hit count:\d+', command_output)
        if len(hits_true) == 0:
            clean_hits.append('0')
        else:
            hit_count = re.findall(r'\d+', hits_true[0])
            clean_hits.append(hit_count[0])
    return clean_hits


## used if choice == "count"; used in get_count()
# generates list of enabled/disabled policy statuses
def status_list():
    print('[*] Working, sending commands, whatever. This takes a little while ...')
    status_list = []
    policy_list = get_policies()
    for policy in policy_list:
        if net_connect.send_command('show firewall policy ' + str(policy) + ' | grep "set status disable"') != '':
            status_list.append('disabled')
        else:
            status_list.append('enabled')
    return status_list


## used if choice == "show"; used in 
# combines status_list with clean_hits to include 'disabled' in place of 0 hits, if policy is disabled
def get_hits():
    i = 0
    policy_status = status_list()
    hit_counts = clean_hits()
    for status in policy_status:
        if status == 'disabled':
            hit_counts[i] = 'disabled'
        i += 1
    return hit_counts


def get_srcintf():
    srcintf_result = []
    clean_srcintf = []
    interface_names = int_names()
    for policy in policy_list:
        result = re.search('set srcintf (.*)$', policy,re.M)
        srcintf_result.append(result.group(0))
    for result in srcintf_result:
        result = result.strip('set srcintf ')
        result = result.replace('"', '')
        if result in interface_names:
            clean_srcintf.append(interface_names[result])
        else:
            clean_srcintf.append(result)
    clean_srcintf.append('any')
    return clean_srcintf


def get_dstintf():
    dstintf_result = []
    clean_dstintf = []
    interface_names = int_names()
    for policy in policy_list:
        result = re.search('set dstintf (.*)$', policy,re.M)
        dstintf_result.append(result.group(0))
    for result in dstintf_result:
        result = result.strip('set dstintf ')
        result = result.replace('"', '')
        if result in interface_names:
            clean_dstintf.append(interface_names[result])
        else:
            clean_dstintf.append(result)
    clean_dstintf.append('any')
    return clean_dstintf


def get_srcaddr():
    srcaddr_result = []
    clean_srcaddr = []
    for policy in policy_list:
        result = re.search('set srcaddr (.*)$', policy,re.M)
        srcaddr_result.append(result.group(0))
    for result in srcaddr_result:
        result = result.strip('set srcaddr ')
        result = result.replace('"', '')
        clean_srcaddr.append(result)
    clean_srcaddr.append('all')
    return clean_srcaddr


def get_dstaddr():
    dstaddr_result = []
    clean_dstaddr = []
    for policy in policy_list:
        result = re.search('set dstaddr (.*)$', policy,re.M)
        dstaddr_result.append(result.group(0))
    for result in dstaddr_result:
        result = result.strip('set dstaddr ')
        result = result.replace('"', '')
        clean_dstaddr.append(result)
    clean_dstaddr.append('all')
    return clean_dstaddr


def get_action():
    clean_action = []
    for policy in policy_list:
        if re.search('set action (.*)$', policy,re.M):
            clean_action.append('accept')
        else:
            clean_action.append('deny')
    clean_action.append('deny')
    return clean_action


def get_schedule():
    schedule_result = []
    clean_schedule = []
    for policy in policy_list:
        result = re.search('set schedule (.*)$', policy,re.M)
        schedule_result.append(result.group(0))
    for result in schedule_result:
        result = result.strip('set schedule ')
        result = result.replace('"', '')
        clean_schedule.append(result)
    clean_schedule.append('always')
    return clean_schedule


def get_service():
    service_result = []
    clean_service = []
    for policy in policy_list:
        result = re.search('set service (.*)$', policy,re.M)
        service_result.append(result.group(0))
    for result in service_result:
        result = result.strip('set service ')
        result = result.replace('"', '')
        clean_service.append(result)
    clean_service.append('ALL')
    return clean_service


def int_names():
    key_result = []
    clean_key = []
    value_result = []
    clean_value = []
    for interface in interface_list:
        if re.search('set alias (.*)$', interface,re.M):
            value = re.search('set alias (.*)$', interface,re.M)
            value_result.append(value.group(0))
            key = re.search('edit (.*)$', interface,re.M)
            key_result.append(key.group(0))
    for result in key_result:
        key = result.strip('edit ')
        key = key.replace('"', '')
        clean_key.append(key)
    for result in value_result:
        value = result.strip('set alias ')
        value = value.replace('"', '')
        clean_value.append(value)
    return dict(zip(clean_key, clean_value))


## used if choice == "count"
# writes policy list and hit counts to CSV
def get_count():
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(zip(get_policies(), get_srcintf(), get_dstintf(), get_srcaddr(), get_dstaddr(), get_schedule(), get_service(), get_action(), get_hits()))


# variable definitions
host_username = sys.argv[1]
choice = sys.argv[2]
host = host_username.partition('@')[2]
username = host_username.partition('@')[0]
password = getpass.getpass(prompt='Password:', stream=None)
filename = host + '_hits.csv'
fortigate = {
    'device_type': 'fortinet',
    'host': host,
    'username': username,
    'password': password,
    'port': 22, # optional, defaults to 22
    'secret': '', # optional, defaults to ''
    }

# logic to determine which commands should be generated/sent
if choice == 'clear':
    base_command = 'di firewall iprope clear 100004'
elif choice == 'count':
    base_command = 'di firewall iprope show 100004'
else:
    sys.exit(1)

# status output
print('[!] Using base command: ' + base_command + '')
print('[*] Connecting. Give it 15 seconds or so ...')
net_connect = ConnectHandler(**fortigate)
print('[+] Successfully connected.')

policy_data = net_connect.send_command('show firewall policy')
policy_list = policy_data.split('next')
policy_list.pop() # extra '\nend\n'
interface_data = net_connect.send_command('show system interface')
interface_list = interface_data.split('next')
interface_list.pop() # extra '\nend\n'

# actually running the functions
if choice == 'clear':
    clear_count()
else:
    print('[!] Name of output file: ' + filename + '')
    get_count()
print('[*] Disconnecting ...')
net_connect.disconnect()
print('[+] Complete.')

# exit
sys.exit(0)
