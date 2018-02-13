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
import math
import data_util
import donor_list
import recipient_list

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
    mapping = {1: 'CMTE_ID',
               8: 'NAME',
               11: 'ZIP_CODE',
               14: 'TRANSACTION_DT',
               15: 'TRANSACTION_AMT',
               16: 'OTHER_ID'
               }    #defines the required database fields
    
    (input_file_name, input_prc_name, output_file_name) = data_util.get_file_names()
    input_prc = data_util.read_percentile(input_prc_name)
    donor_list = donor_list.Donor_list(did = 'DONOR_ID', dyear = 'TRANSACTION_DT')
    recipient_list = recipient_list.Recipient_list('RECIPIENT_ID', 'TRANSACTION_AMT')

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