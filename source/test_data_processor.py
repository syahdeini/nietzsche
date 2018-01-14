import unittest
from unittest.mock import patch
import numpy
import pandas as pd
from data_processor import *
import os
from datetime import datetime

class TestData_processor(unittest.TestCase):

   def setUp(self):
       arr = numpy.array([['cs1','ord1',1,100.5,'2017-07-01'],['cs1','ord1',5,200.5,'2017-06-01']])
       _columns = ['customer_id','order_id','num_items','revenue','created_at_date']
       self.dataframe = pd.DataFrame(arr,columns=_columns)
       # in the csv folder it can read the field as float
       # but here it can't so we need to typecast it
       self.dataframe['revenue'] = pd.to_numeric(self.dataframe['revenue'],downcast='float')
       self.OOT_DIR = os.path.dirname(os.path.abspath(__file__))

   def test_load_data_file(self):
       dataset = load_data_file()
       self.assertNotEqual(len(dataset),0)
       print("finish test load_data_file")

   def test_max_num_items(self):
       dataset_return = max_num_items(self.dataframe)
       num_items = dataset_return.iloc[0]['num_items_sum']
       self.assertEqual(int(num_items),5)
       print("finish max_num_items")
       
   def test_max_revenue(self):
       dataset_return = max_revenue(self.dataframe)
       revenue = dataset_return.iloc[0]['revenue_max']
       self.assertEqual(revenue,200.5)
       print("finish max_revenue")

   def test_total_revenue(self):
       dataset_return = total_revenue(self.dataframe)
       revenue = dataset_return.iloc[0]['revenue_total']
       self.assertEqual(revenue,301)
       print("finish test total_revenue") 

   def test_total_orders(self):
       dataset_return = total_orders(self.dataframe)
       total_order = dataset_return.iloc[0]['order_id_total']
       self.assertEqual(int(total_order),2)
       print("finish test total orders")

   def get_date_gap(self,date_str_1, date_str_2):
       date1 = datetime.strptime(date_str_1,"%Y-%m-%d")
       date2 = datetime.strptime(date_str_2,"%Y-%m-%d")
       return abs((date2-date1).days)
       
   def test_day_since_last_order(self):
       dataset_return = day_since_last_order(self.dataframe)
       days_gap = dataset_return.iloc[0]['day_since_last_order']
       max_date = dataset_return['created_at_date'].max()
       real_days_gap = self.get_date_gap("2017-10-17", max_date)
       self.assertEqual(days_gap, real_days_gap)
       print("finish test day_since_last_order")

   def test_two_consecutive_order(self):
       dataset_return = day_since_last_order(self.dataframe)
       dataset_return = two_consecutive_order(dataset_return)
       days_gap = dataset_return.iloc[0]['gap_days']
       max_date = dataset_return['created_at_date'].max()
       min_date = dataset_return['created_at_date'].min()
       real_days_gap = self.get_date_gap(max_date, min_date)
       self.assertEqual(days_gap, real_days_gap)
       print("finish test two_consecutive_order")

if __name__ == '__main__':
    unittest.main()
