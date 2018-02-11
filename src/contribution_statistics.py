# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 22:51:35 2018

@author: Anna Epishova
"""

import csv
import os.path
import re
import bisect
import math
import decimal

def round_up(number):
    """
    Round to nearest with ties going away from zero.
    """
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    return int(round(decimal.Decimal(number), 0))


def extract_fields(row, mapping):
    """
    Extract required fields from a row.
    """
    cols = {}    
    for field in mapping:
        cols[mapping[field]] = row[field - 1]
    return cols


def row_valid(cols):
    """Define necessary row checks in this procedure.
    """
    #Define a pattern to check validity of person names below. 
    #Here we allow names like "Jr. Name" or "Name 2", which may be used insted of "Name II":
    name_pattern = '^[a-zA-Z]+[a-zA-Z0-9\s\.\,]*$'
    dt_pattern = '^[\d]{8}$'
    zip_pattern = '^[\d]{5,}$'
    amt_pattern = '^[\d]+$'
    
    if cols['CMTE_ID'] == '' or \
        re.match(amt_pattern, cols['TRANSACTION_AMT']) is None or \
        cols['OTHER_ID'] != '' or \
        re.match(name_pattern, cols['NAME']) is None or \
        re.match(dt_pattern, cols['TRANSACTION_DT']) is None or \
        re.match(zip_pattern, cols['ZIP_CODE']) is None:
            return False
    else:
        return True
    
    
def transform_fields(cols):
    """
    Transform existing fields as required and add new fields if needed
    """
    cols['ZIP_CODE'] = cols['ZIP_CODE'][0:5]
    cols['TRANSACTION_DT'] = cols['TRANSACTION_DT'][-4:]
    cols['DONOR_ID'] = cols['ZIP_CODE'] + cols['NAME']
    cols['RECIPIENT_ID'] = cols['CMTE_ID'] + cols['ZIP_CODE'] + cols['TRANSACTION_DT']
    cols['TRANSACTION_DT'] = int(cols['TRANSACTION_DT'])
    cols['TRANSACTION_AMT'] = int(cols['TRANSACTION_AMT'])


def add_donor(cols, donor_list):
    """ Add a new donor with the corresponding year of the first donation.
    Set a boolean flag that it is not a repeated donor
    """
    donor_list[cols['DONOR_ID']] = [cols['TRANSACTION_DT'], False]

    
def compute_repdonor_stat(cols, donor_list):    
    """
    For a repeat donor return the amount of donation.
    A donor is considered as being repeat since a year when we encountered his/her 
    second donation. If needed, we update that year to the earlier timestamp.
    """
    if not donor_list[cols['DONOR_ID']][1]:
        donor_list[cols['DONOR_ID']][1] = True
    if donor_list[cols['DONOR_ID']][0] > cols['TRANSACTION_DT']:
        donor_list[cols['DONOR_ID']][0] = cols['TRANSACTION_DT']
        return False
    else:
        return True

    
def compute_recipient_stat(cols, recipient_list, prc):
    """Update and return required statistic for the given recipient.
    """
    if cols['RECIPIENT_ID'] not in recipient_list:
        recipient_list[cols['RECIPIENT_ID']] = [0, 0, [], cols['TRANSACTION_AMT']]
    recipient_list[cols['RECIPIENT_ID']][0] += 1
    recipient_list[cols['RECIPIENT_ID']][1] += cols['TRANSACTION_AMT']
    prc_amt = recipient_list[cols['RECIPIENT_ID']][3]
    
    n = math.ceil(prc * recipient_list[cols['RECIPIENT_ID']][0])
    if (n != math.ceil(prc * (recipient_list[cols['RECIPIENT_ID']][0] - 1)) or
        cols['TRANSACTION_AMT'] < recipient_list[cols['RECIPIENT_ID']][3]):
        bisect.insort(recipient_list[cols['RECIPIENT_ID']][2], cols['TRANSACTION_AMT'])
        prc_amt = recipient_list[cols['RECIPIENT_ID']][2][n - 1]
        recipient_list[cols['RECIPIENT_ID']][3] = prc_amt
    return (round_up(prc_amt), recipient_list[cols['RECIPIENT_ID']][1], recipient_list[cols['RECIPIENT_ID']][0])

    
def read_percentile(input_prc_name):
    """
    Read the value of percentile from the input file
    """
    input_prc = 0
    with open(input_prc_name, 'r') as input_prc:
        reader = csv.reader(input_prc)
        for row in reader:
            input_prc = float(row[0])
    if (input_prc < 0 or input_prc > 100):
        raise ValueError('Percentile value is out of range')         
    return input_prc / 100

    
mapping = {1: 'CMTE_ID',
           8: 'NAME',
           11: 'ZIP_CODE',
           14: 'TRANSACTION_DT',
           15: 'TRANSACTION_AMT',
           16: 'OTHER_ID'
           }
    
src_path = os.path.abspath(os.path.dirname(__file__))
input_file_name = os.path.join(src_path, '../input/itcont.txt')
input_prc_name = os.path.join(src_path, '../input/percentile.txt')
output_file_name = os.path.join(src_path, '../output/repeat_donors.txt')

#input_prc = 0
#with open(input_prc_name, 'r') as input_prc:
#    reader = csv.reader(input_prc)
#    for row in reader:
#        input_prc = float(row[0])
#if (input_prc < 0 or input_prc > 100):
#    raise ValueError('Percentile value is out of range')         
#input_prc = input_prc / 100
input_prc = read_percentile(input_prc_name)
donor_list = {}
recipient_list = {} 

output_file = open(output_file_name, "w") 
with open(input_file_name, 'r') as input_file:
    reader = csv.reader(input_file, delimiter = '|')
    for row in reader:
        cols = extract_fields(row, mapping)
        if not row_valid(cols):
            continue
        transform_fields(cols)
        if cols['DONOR_ID'] not in donor_list:
            add_donor(cols, donor_list)
        else:
            if compute_repdonor_stat(cols, donor_list):
                stat = compute_recipient_stat(cols, recipient_list, input_prc)
                output_row = cols['CMTE_ID'] + '|' + cols['ZIP_CODE'] + '|' + str(cols['TRANSACTION_DT']) + '|'
                output_row += '|'.join(str(val) for val in stat) + '\n'
                output_file.write(output_row)
output_file.close()
