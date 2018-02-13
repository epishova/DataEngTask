# -*- coding: utf-8 -*-
"""
Unit tests for data_util, donor_list
"""
import unittest
import os
from data_util import round_up, extract_fields, row_valid, transform_fields, read_percentile
import donor_list
import recipient_list

class Test_data_util(unittest.TestCase):
    """Test data_util module
    """
    def test_round_up(self):
        res = round_up(0.5)
        self.assertEqual(res, 1)

    def test_extract_fields(self):
        mapping = {1: 'a',
                   2: 'b',
                   5: 'c'}
        row = [1, 2, 3, 4, 5]
        cols = {'a': 1, 'b': 2, 'c': 5}
        res = extract_fields(row, mapping)
        self.assertEqual(res, cols)
        with self.assertRaises(IndexError):
            res = extract_fields([1, 2, 3], mapping)
            
    def test_row_valid(self):
        cols = {'CMTE_ID': 'id',
                'TRANSACTION_AMT': '123',
                'OTHER_ID': '',
                'NAME': 'Name',
                'TRANSACTION_DT': '01012018',
                'ZIP_CODE': '123456'}
        self.assertTrue(row_valid(cols))
        cols['OTHER_ID'] = '123'
        self.assertFalse(row_valid(cols))
        cols['OTHER_ID'] = ''
        cols['NAME'] = 'Invalid / Name'
        self.assertFalse(row_valid(cols))
        cols['NAME'] = 'Jr. Name 2'
        cols['TRANSACTION_DT'] = ''
        self.assertFalse(row_valid(cols))
        
    
    def test_transform_fields(self):
        cols = {'CMTE_ID': 'id',
                'TRANSACTION_AMT': '123',
                'OTHER_ID': '',
                'NAME': 'Name',
                'TRANSACTION_DT': '01012018',
                'ZIP_CODE': '123456'}
        res = {'CMTE_ID': 'id',
               'DONOR_ID': '12345Name',
               'NAME': 'Name',
               'OTHER_ID': '',
               'RECIPIENT_ID': 'id123452018',
               'TRANSACTION_AMT': 123,
               'TRANSACTION_DT': 2018,
               'ZIP_CODE': '12345'}
        transform_fields(cols)
        self.assertEqual(cols, res)
        
        
    def test_read_percentile(self):
        src_path = os.path.abspath(os.path.dirname(__file__))
        input_prc_name = os.path.join(src_path, '../input/somefile.txt')
        with self.assertRaises(FileNotFoundError):
            read_percentile(input_prc_name)
        

class Test_donor_list(unittest.TestCase):
    """Test donor_list
    """
    def setUp(self):
        self.donor_list = donor_list.Donor_list('id', 'year')
 
    def test_add_donor(self):
        self.assertFalse(self.donor_list.exists('1'))
        cols = {'id': '1',
                'year': '2018'}
        self.donor_list.add_donor(cols)
        self.assertTrue(self.donor_list.exists('1'))

    def test_repeat_donor(self):
        cols = {'id': '1',
                'year': '2018'}
        self.assertFalse(self.donor_list.repeat_donor(cols))
        self.donor_list.add_donor(cols)
        self.assertTrue(self.donor_list.repeat_donor(cols))
        cols = {'id': '1',
                'year': '2017'}
        self.assertFalse(self.donor_list.repeat_donor(cols))
        self.assertTrue(self.donor_list.repeat_donor(cols))


class Test_recipient_list(unittest.TestCase):
    """Test donor_list
    """
    def setUp(self):
        self.rec_list = recipient_list.Recipient_list('id', 'amt')
 
    def test_add_recipient(self):
        self.assertFalse(self.rec_list.exists('1'))
        self.rec_list.add_recipient('1')
        self.assertTrue(self.rec_list.exists('1'))
        
    def test_add_donation(self):
        self.assertFalse(self.rec_list.exists('1'))
        cols = {'id': '1',
                'amt': 100}
        self.rec_list.add_recipient(cols['id'])
        self.assertTrue(self.rec_list.exists(cols['id']))
        self.assertEqual(self.rec_list.get_donation_count(cols['id']), 0)
        self.assertEqual(self.rec_list.get_donation_amount(cols['id']), 0)
        self.rec_list.add_donation(cols)
        self.assertEqual(self.rec_list.get_donation_count(cols['id']), 1)
        self.assertEqual(self.rec_list.get_donation_amount(cols['id']), cols['amt'])
        cols1 = {'id': '2',
                'amt': 200}
        self.rec_list.add_recipient(cols1['id'])
        self.assertTrue(self.rec_list.exists(cols1['id']))
        self.assertEqual(self.rec_list.get_donation_count(cols1['id']), 0)
        self.assertEqual(self.rec_list.get_donation_amount(cols1['id']), 0)
        self.assertEqual(self.rec_list.get_donation_count(cols['id']), 1)
        self.assertEqual(self.rec_list.get_donation_amount(cols['id']), cols['amt'])
        self.rec_list.add_donation(cols1)
        self.assertEqual(self.rec_list.get_donation_count(cols1['id']), 1)
        self.assertEqual(self.rec_list.get_donation_amount(cols1['id']), cols1['amt'])
        self.assertEqual(self.rec_list.get_donation_count(cols['id']), 1)
        self.assertEqual(self.rec_list.get_donation_amount(cols['id']), cols['amt'])

        
    def test_set_percentile(self):
        self.assertFalse(self.rec_list.exists('1'))
        cols = {'id': '1',
                'amt': 100}
        self.rec_list.add_recipient(cols['id'])
        self.assertTrue(self.rec_list.exists(cols['id']))
        self.rec_list.add_donation(cols)
        self.rec_list.set_percentile(cols['id'], 1)
        self.assertEqual(self.rec_list.get_percentile(cols['id']), cols['amt'])
        cols1 = {'id': '1',
                'amt': 200}
        self.rec_list.add_donation(cols1)
        self.assertEqual(self.rec_list.get_percentile(cols1['id']), cols['amt'])
        self.rec_list.set_percentile(cols1['id'], 2)
        self.assertEqual(self.rec_list.get_percentile(cols1['id']), cols1['amt'])

       
if __name__ == '__main__':
    unittest.main()