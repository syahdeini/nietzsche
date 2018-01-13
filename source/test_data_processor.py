import unittest
from unittest.mock import patch
import numpy
import pandas as pd
from data_processor import *
import os


class TestData_processor(unittest.TestCase):

   def setUp(self):
       arr = numpy.array([['cs1','ord1',1,100,'2017-07-01'],['cs1','ord1',5,200,'2017-07-10']])
       _columns = ['customer_id','order_id','num_items','revenue','created_at']
       self.dataframe = pd.DataFrame(arr,columns=_columns)
       
       #numpy.array([[3,92.6,109.3,2,12,26],[2,10.4,43.5,3,26,5]]) 
       self.OOT_DIR = os.path.dirname(os.path.abspath(__file__))

   def test_load_data_file(self):
       dataset = load_data_file()
       self.assertNotEqual(len(dataset),0)

   def test_max_num_items(self):
       dataset_return = max_num_items(self.dataframe)
       num_items = dataset_return.iloc[0]['num_items_sum']
       self.assertEqual(int(num_items),5)
       
   def test_max_revenue(self)
       dataset_return = max_revenue(self.dataframe)
       num_items = dataset_return.iloc[0]['revenue_max']
       self.assertEqual(int(num_items),5)
       


#
#dataset = numpy.array([[3,92.6,109.3,2,12,26],[2,10.4,43.5,3,26,5]]) 
 #     self.mocked_load_data = patch('load_data_file')
    #  self.mocked_load_data.return_value = dataset
        
if __name__ == '__main__':
    unittest.main()
