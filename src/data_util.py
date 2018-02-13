# -*- coding: utf-8 -*-
"""
Utilities for input data cleaning and transforming.
"""
import csv
import re
import decimal
import sys
import os

def round_up(number):
    """Round to nearest with ties going away from zero.
    """
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    return int(round(decimal.Decimal(number), 0))


def extract_fields(row, mapping):
    """Extract required fields from a row.
    """
    cols = {}    
    for field in mapping:
        cols[mapping[field]] = row[field - 1]
    return cols


def row_valid(cols):
    """Defines necessary row validation checks.
    """
    #Define a pattern to check the validity of a person's name:
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
    """Modify database fields.
    """
    cols['ZIP_CODE'] = cols['ZIP_CODE'][0:5]
    cols['TRANSACTION_DT'] = cols['TRANSACTION_DT'][-4:]
    cols['DONOR_ID'] = cols['ZIP_CODE'] + cols['NAME']
    cols['RECIPIENT_ID'] = cols['CMTE_ID'] + cols['ZIP_CODE'] + cols['TRANSACTION_DT']
    cols['TRANSACTION_DT'] = int(cols['TRANSACTION_DT'])
    cols['TRANSACTION_AMT'] = int(cols['TRANSACTION_AMT'])


def read_percentile(input_prc_name):
    """Read the percentile value from the input file
    """
    input_prc = 0
    with open(input_prc_name, 'r') as input_prc:
        reader = csv.reader(input_prc)
        for row in reader:
            input_prc = float(row[0])
    if (input_prc < 0 or input_prc > 100):
        raise ValueError('Percentile value is out of range')         
    return input_prc / 100

def get_file_names():
    """Retearn file names given as command line arguments
    """
    if len(sys.argv) < 4:
        src_path = os.path.abspath(os.path.dirname(__file__))
        input_file_name = os.path.join(src_path, '../input/itcont.txt')
        input_prc_name = os.path.join(src_path, '../input/percentile.txt')
        output_file_name = os.path.join(src_path, '../output/repeat_donors.txt')
    else:    
        input_file_name = str(sys.argv[1])
        input_prc_name = str(sys.argv[2])
        output_file_name = str(sys.argv[3])
    return(input_file_name, input_prc_name, output_file_name)