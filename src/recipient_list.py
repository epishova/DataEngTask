# -*- coding: utf-8 -*-
"""
This class defines a list of recipients.
"""
import bisect

class Recipient_list():
    """Each recipient is defined by its id. 
    Each record contains the number of transactions, total amount, 
    list of donations, and the current value of running percentile 
    """
    def __init__(self, rid, amt):
        """Define field names which will be used to refer to the recipient's id and the
        transaction amount.
        """
        self.rec_list = {}
        self.rid = rid
        self.amt = amt
        
    def exists(self, rec_id):
        """Return True is rec_id exists in the recipient list
        """
        return (rec_id in self.rec_list)
       
    def add_recipient(self, rec_id):
        """ Add a new recipient.
        """
        self.rec_list[rec_id] = [0, 0, [], 0]
        
    def add_donation(self, cols):    
        """Add information about donation to the corresponding recipient.
        """
        self.rec_list[cols[self.rid]][0] += 1
        self.rec_list[cols[self.rid]][1] += cols[self.amt]
        #Insert new donation into the ordered list:
        bisect.insort(self.rec_list[cols[self.rid]][2], cols[self.amt])

    def get_donation_count(self, rid):
        """Return the current number of donations received by a cpecified recipient.
        """
        return self.rec_list[rid][0]
    
    def get_donation_amount(self, rid):
        """Return the current amount of donations received by a cpecified recipient.
        """
        return self.rec_list[rid][1]

    def get_percentile(self, rid):
        """Return the current value of percentile for a cpecified recipient.
        """
        return self.rec_list[rid][3]
    
    def set_percentile(self, rid, prc_rank):
        """Update the current value of percentile value for a cpecified recipient.
        """
        self.rec_list[rid][3] = self.rec_list[rid][2][prc_rank - 1]