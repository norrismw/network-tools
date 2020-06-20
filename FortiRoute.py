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
    
    
def sequence_num_list(load):
    sequence_num_list = []
    c = 1
    for i in range(len(load)):
        if i == 0:
            sequence_num = "edit {}".format(seq_number)
            sequence_num_list.append(sequence_num)
        else:
            sequence_num = "edit {}".format(int(seq_number) + c)
            sequence_num_list.append(sequence_num)
            c += 1
    return sequence_num_list
    

def replace_sequence(sequence_num_list):
    return [base_template.replace('edit seq_number', str(sequence_num_list[i])) for i in range(len(sequence_num_list))]
    

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
seq_number = input("Starting sequence number: ")
outgoing_interface = input("Outgoing interface (device): ")
cust_comment = input("Comment: ")

base_template = """edit seq_number
    set dst dest_subnet
    set device "{a}"
    set comment "{b}"
next\n""".format(a = outgoing_interface, b = cust_comment)

load = load_from_csv('{}'.format(fp))
s2 = sequence_num_list(load)
s3 = replace_sequence(s2)
final = replace_dest(s3)

filename = outgoing_interface + '_routes.txt'

with open(filename, 'w') as f:
        for i in final:
            f.write(i)
print("Output file: {}".format(filename))
