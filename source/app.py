import os
import sys
import dill
import numpy as np
from data_processor import *

def load_model(path="../model/model.dill"):
    #print("loading model "+path)
    with open(path, 'rb') as f:
        model = dill.load(f)
        return model

#def load_data_file(path="../data/orders.csv"):
#    return genfromtxt(path, delimiter=',',dtype=str,skip_header=1)
    
def process_to_save_dataset():
    dataset = load_data_file()
    dataset = max_num_items(dataset)
    dataset = max_revenue(dataset)
    dataset = total_revenue(dataset)
    dataset = total_orders(dataset)
    dataset = day_since_last_order(dataset)
    dataset = two_consecutive_order(dataset)
    datetime_now = datetime.now().strftime("%B_%d_%Y")
    output_path = "/home/bukalapak/nietzsche/warehouse/datadump_{}.csv".format(datetime_now)
    dataset.to_csv(output_path, sep=",")
    return dataset 


def get_row_from_data(dataset, customer_id):
    row = dataset.loc[dataset['customer_id']==customer_id]
    row = row[['num_items_sum','revenue_max','revenue_total','order_id_total', 'day_since_last_order', 'gap_days']].values
    return row





model = load_model()
dataset = process_to_save_dataset()
row_arrays = get_row_from_data(dataset,"450e1c2cbd21687780153995f1be0c23")
result = model.predict(row_arrays)
#dataset = load_data_file()
#result = model.predict(dataset

