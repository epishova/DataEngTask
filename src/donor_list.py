# -*- coding: utf-8 -*-
"""
This class defines a list of donors.
"""

class Donor_list():
    """Each donor is defined by its id. 
    Each record contains the corresponding year of the donor's first donation.
    """
    def __init__(self, did, dyear):
        """Define field names which will be used to refer to the donor's id and the
        correcsponding year.
        """
        self.donor_list = {}
        self.did = did
        self.dyear = dyear
        
        
    def exists(self, donor_id):
        """Return True is donor_id exists in the donor list
        """
        return (donor_id in self.donor_list)

        
    def add_donor(self, cols):
        """ Add a new donor with the corresponding year of his first donation.
        """
        self.donor_list[cols[self.did]] = cols[self.dyear]
    
        
    def repeat_donor(self, cols):    
        """Return True for a repeat donor.
        """
        if not self.exists(cols[self.did]):
            return False
        
        if self.donor_list[cols[self.did]] > cols[self.dyear]:
            self.donor_list[cols[self.did]] = cols[self.dyear]
            return False
        else:
            return True        