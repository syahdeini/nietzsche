import unittest
from unittest.mock import patch
from unittest import mock
import numpy
import numpy.testing as np_test
import pandas as pd
from app import *
import os
from datetime import datetime
import asyncio

#import data_processor

class TestApp(unittest.TestCase):

   @classmethod 
   def setUpClass(cls):
      arr = numpy.array([['cs1','ord1',1, float(100.5),'2017-07-01'],['cs1','ord1',5, float(200.5),'2017-06-01']])

      _columns = ['customer_id','order_id','num_items','revenue','created_at_date']
      cls.dataframe = pd.DataFrame(arr,columns=_columns)
      cls.dataframe['revenue'] = pd.to_numeric(cls.dataframe['revenue'],downcast='float')
      cls.dataframe['num_items'] =  pd.to_numeric(cls.dataframe['num_items'])

      cls.dataframe_processed = process_to_save_dataset(cls.dataframe)
      cls.true_clv = numpy.array([646.5,646.5])
      print("successfuly set up class environment")

   def setUp(self):
      self.assertIsNotNone(model)
      self.assertIsNotNone(dataset)
      self.assertIsInstance(dataset,pd.core.frame.DataFrame)
      print("Successful load model and dataset")

   def test_load_model(self):
        # test load model again
        _model = load_model(model)
        self.assertIsNotNone(_model)
        print("succesfully test_load_model")

   def test_load_dataset(self):
        # test load dataset again
        _dataset = load_dataset(dataset)
        self.assertIsNotNone(_dataset)
        print("successfuly test load dataset")

   def test_process_to_save_dataset(self):
        dataset = process_to_save_dataset()
        self.assertIsNotNone(dataset)
        self.assertIsInstance(dataset,pd.core.frame.DataFrame)
        print("successfuly test process_to_save_dataset")

   def test_get_row_from_data(self):
        rows = get_row_from_data(self.dataframe_processed,"cs1")
        true_return = numpy.array([[5, 200.5, 301.0, 2, 108, 30.0],[5, 200.5, 301.0, 2, 108, 30.0]])
        self.assertEqual(rows.tolist(),true_return.tolist())
        print("successfully test get_row_from_data")

   def test_calculate_customer_clv(self):
       cal_clv = calculate_customer_clv(self.dataframe_processed, model, 'cs1')
       clv = asyncio.get_event_loop().run_until_complete(cal_clv)
       self.assertEqual(clv.tolist(),self.true_clv.tolist())
       print("successfully test calculate_customer_clv")

   class Fake_request:
      def __init__(self):
          self.json = {'customer_id':'cs1'}

   @mock.patch('app.calculate_customer_clv')
   def test_get_clv(self,mock_get_clv):
       async def fake_calculate_customer_clv():
          return self.true_clv
      #mock_get_clv.calculate_customer_clv = self.true_clv
       mock_get_clv.return_value = fake_calculate_customer_clv()
       fake_request = self.Fake_request()
       self.dataframe_processed
       cal_get_clv = get_clv(fake_request)
       clv = asyncio.get_event_loop().run_until_complete(cal_get_clv)
       print("successfully test get_clv")
  
   def test_refresh_data(self):
       fake_request = self.Fake_request()
       cal_refresh_data = refresh_data(fake_request)
       ret_value = asyncio.get_event_loop().run_until_complete(cal_refresh_data)
       self.assertEqual(ret_value.status,200)
       print("succesfully test refresh_data")

if __name__ == '__main__':
    unittest.main()
