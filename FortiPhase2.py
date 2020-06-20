#!/usr/bin/python3
import csv
import sys


def load_from_csv(filename):
    lines = []
    with open(filename) as f:
        f = (line.strip() for line in f)
        f = csv.reader(f)
        for line in f:
            lines.append(line)
    return lines
    
    
def cust_name_list(load):
    customer_names = []
    for i in range(len(load)):
        if i == 0:
            name = "{}".format(phase1name)
            customer_names.append(name)
        else:
            name = "{a}{b}".format(a = phase1name, b = i)
            customer_names.append(name)
    return customer_names
    

def replace_name(cust_names):
    return [base_template.replace('Customer_Name', str(cust_names[i])) for i in range(len(cust_names))]
    

def replace_source(input_list):
    source_replace = []
    c = 0
    while c < len(input_list):
        for i in input_list:
            add = i.replace('source_subnet', str(load[c][0]))
            source_replace.append(add)
            c += 1
    return source_replace
    
    
def replace_dest(input_list):
    dest_replace = []
    c = 0
    while c < len(input_list):
        for i in input_list:
            add = i.replace('dest_subnet', str(load[c][1]))
            dest_replace.append(add)
            c += 1
    return dest_replace
    
    
fp = input("Path to CSV file: ")
phase1name = input("phase1name: ")
proposal = input("propsal: ")
keylifeseconds = input("keylifeseconds: ")

base_template = """edit "Customer_Name"
    set phase1name "{a}"
    set proposal {b}
    set pfs disable
    set replay disable
    set keylifeseconds {c}
    set src-subnet source_subnet
    set dst-subnet dest_subnet
next\n""".format(a = phase1name, b = proposal, c = keylifeseconds)

load = load_from_csv('{}'.format(fp))
s2 = cust_name_list(load)
s3 = replace_name(s2)
s4 = replace_source(s3)
final = replace_dest(s4)
filename = phase1name + '_phase2.txt'

with open(filename, 'w') as f:
        for i in final:
            f.write(i)
print("Output file: {}".format(filename))
