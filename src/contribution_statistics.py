# -*- coding: utf-8 -*-
"""
For each recipient, zip code and calendar year, calculate the following values 
for contributions coming from repeat donors:
1. total dollars received
2. total number of contributions received
3. donation amount in a given percentile

Accept input/output file names from the command line.
By default use the following input files: 
../input/itcont.txt
../input/percentile.txt
and output results to:
../output/repeat_donors.txt
"""
import csv
import os.path
#import re
#import bisect
import math
import data_util
import donor_list
import recipient_list
#import decimal
#
#def round_up(number):
#    """Round to nearest with ties going away from zero.
#    """
#    context = decimal.getcontext()
#    context.rounding = decimal.ROUND_HALF_UP
#    return int(round(decimal.Decimal(number), 0))


#def extract_fields(row, mapping):
#    """Extract required fields from a row.
#    """
#    cols = {}    
#    for field in mapping:
#        cols[mapping[field]] = row[field - 1]
#    return cols
#
#
#def row_valid(cols):
#    """Defines necessary row validation checks.
#    """
#    #Define a pattern to check the validity of a person's name:
#    #Here we allow names like "Jr. Name" or "Name 2", which may be used insted of "Name II":
#    name_pattern = '^[a-zA-Z]+[a-zA-Z0-9\s\.\,]*$'
#    dt_pattern = '^[\d]{8}$'
#    zip_pattern = '^[\d]{5,}$'
#    amt_pattern = '^[\d]+$'
#    
#    if cols['CMTE_ID'] == '' or \
#        re.match(amt_pattern, cols['TRANSACTION_AMT']) is None or \
#        cols['OTHER_ID'] != '' or \
#        re.match(name_pattern, cols['NAME']) is None or \
#        re.match(dt_pattern, cols['TRANSACTION_DT']) is None or \
#        re.match(zip_pattern, cols['ZIP_CODE']) is None:
#            return False
#    else:
#        return True
#    
#    
#def transform_fields(cols):
#    """Modify database fields.
#    """
#    cols['ZIP_CODE'] = cols['ZIP_CODE'][0:5]
#    cols['TRANSACTION_DT'] = cols['TRANSACTION_DT'][-4:]
#    cols['DONOR_ID'] = cols['ZIP_CODE'] + cols['NAME']
#    cols['RECIPIENT_ID'] = cols['CMTE_ID'] + cols['ZIP_CODE'] + cols['TRANSACTION_DT']
#    cols['TRANSACTION_DT'] = int(cols['TRANSACTION_DT'])
#    cols['TRANSACTION_AMT'] = int(cols['TRANSACTION_AMT'])


#def add_donor(cols, donor_list):
#    """ Add a new donor with the corresponding year of his first donation.
#    """
#    donor_list[cols['DONOR_ID']] = cols['TRANSACTION_DT']
#
#    
#def repeat_donor(cols, donor_list):    
#    """Return True for a repeat donor.
#    """
#    if donor_list[cols['DONOR_ID']] > cols['TRANSACTION_DT']:
#        donor_list[cols['DONOR_ID']] = cols['TRANSACTION_DT']
#        return False
#    else:
#        return True

    
#def compute_recipient_stat(cols, recipient_list, prc):
#    """Update and return required statistic for the given recipient.
#    """
#    if cols['RECIPIENT_ID'] not in recipient_list:
#        #For each recipient ID, we store number of transactions, total amount, 
#        #list of donations, and the current value of running percentile:  
#        recipient_list[cols['RECIPIENT_ID']] = [0, 0, [], cols['TRANSACTION_AMT']]
#        
#    recipient_list[cols['RECIPIENT_ID']][0] += 1
#    recipient_list[cols['RECIPIENT_ID']][1] += cols['TRANSACTION_AMT']
#    prc_amt = recipient_list[cols['RECIPIENT_ID']][3]
#    
#    #If the nearest-rank n has changed, or the value of current percentile donation
#    #has moved in the list, then update the value of current percentile donation:
#    n = math.ceil(prc * recipient_list[cols['RECIPIENT_ID']][0])
#    if (n != math.ceil(prc * (recipient_list[cols['RECIPIENT_ID']][0] - 1)) or
#        cols['TRANSACTION_AMT'] < recipient_list[cols['RECIPIENT_ID']][3]):
#        #Insert new donation into the ordered list.
#        bisect.insort(recipient_list[cols['RECIPIENT_ID']][2], cols['TRANSACTION_AMT'])
#        prc_amt = recipient_list[cols['RECIPIENT_ID']][2][n - 1]
#        recipient_list[cols['RECIPIENT_ID']][3] = prc_amt
#    return (data_util.round_up(prc_amt), recipient_list[cols['RECIPIENT_ID']][1], recipient_list[cols['RECIPIENT_ID']][0])

    
#def read_percentile(input_prc_name):
#    """Read the percentile value from the input file
#    """
#    input_prc = 0
#    with open(input_prc_name, 'r') as input_prc:
#        reader = csv.reader(input_prc)
#        for row in reader:
#            input_prc = float(row[0])
#    if (input_prc < 0 or input_prc > 100):
#        raise ValueError('Percentile value is out of range')         
#    return input_prc / 100
def compute_recipient_stat(cols, recipient_list, prc):
    """Update and return required statistic for the given recipient.
    """
    if not recipient_list.exists(cols['RECIPIENT_ID']):
        recipient_list.add_recipient(cols['RECIPIENT_ID'])
        
    recipient_list.add_donation(cols)
    
    #If the nearest-rank n has changed, or the value of current percentile donation
    #has moved in the list, then update the value of current percentile donation:
    n = recipient_list.get_donation_count(cols['RECIPIENT_ID'])
    if (math.ceil(prc * n) != math.ceil(prc * (n - 1)) or
        cols['TRANSACTION_AMT'] < recipient_list.get_percentile(cols['RECIPIENT_ID'])):
        recipient_list.set_percentile(cols['RECIPIENT_ID'], math.ceil(prc * n))

    return (data_util.round_up(recipient_list.get_percentile(cols['RECIPIENT_ID'])), 
            recipient_list.get_donation_amount(cols['RECIPIENT_ID']), 
            n)

if __name__ == '__main__':    
    #Define the required input parameters below:
    #mapping: this variable defines the required database fields
    #input_*_name: those variables define locations and names of the input/ouput files
    mapping = {1: 'CMTE_ID',
               8: 'NAME',
               11: 'ZIP_CODE',
               14: 'TRANSACTION_DT',
               15: 'TRANSACTION_AMT',
               16: 'OTHER_ID'
               }
    
    (input_file_name, input_prc_name, output_file_name) = data_util.get_file_names()
#    src_path = os.path.abspath(os.path.dirname(__file__))
#    input_file_name = os.path.join(src_path, '../input/itcont.txt')
#    input_prc_name = os.path.join(src_path, '../input/percentile.txt')
#    output_file_name = os.path.join(src_path, '../output/repeat_donors.txt')
    
    #Variables initialization section:
    input_prc = data_util.read_percentile(input_prc_name)
    donor_list = donor_list.Donor_list(did = 'DONOR_ID', dyear = 'TRANSACTION_DT') #{}     #list of all donors
    recipient_list = recipient_list.Recipient_list('RECIPIENT_ID', 'TRANSACTION_AMT')  #{} #list of recipiens for whome the donation statistics were gathered 

    output_file = open(output_file_name, "w") 
    with open(input_file_name, 'r') as input_file:
        reader = csv.reader(input_file, delimiter = '|')
        for row in reader:
            #clean input data:
            cols = data_util.extract_fields(row, mapping)
            if not data_util.row_valid(cols):
                continue
            data_util.transform_fields(cols)
            #maintain donor list:
            #if cols['DONOR_ID'] not in donor_list:
            if not donor_list.exists(cols['DONOR_ID']):
                donor_list.add_donor(cols)
            else:
                #for a repeat donor output statistics for the corresponding reciipient:
                if donor_list.repeat_donor(cols):
                    stat = compute_recipient_stat(cols, recipient_list, input_prc)
                    output_row = cols['CMTE_ID'] + '|' + cols['ZIP_CODE'] + '|' + str(cols['TRANSACTION_DT']) + '|'
                    output_row += '|'.join(str(val) for val in stat) + '\n'
                    output_file.write(output_row)
    output_file.close()