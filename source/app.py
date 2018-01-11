import os
import sys
import dill
import numpy as np
from data_processor import *
from sanic.exceptions import RequestTimeout, NotFound
from sanic.response import json
from sanic import Sanic, response
import asyncio

app = Sanic()
loop = asyncio.get_event_loop()
OOT_DIR = os.path.dirname(os.path.abspath(__file__))
def load_model(model, path=OOT_DIR+"/../model/model.dill"):
    if model:
        print("model already loaded")
        return model
    print("loading model "+path)
    with open(path, 'rb') as f:
        model = dill.load(f)
    print("finish load model")    
    return model
    
#def load_data_file(path="../data/orders.csv"):
#    return genfromtxt(path, delimiter=',',dtype=str,skip_header=1)


def load_dataset(dataset):
   print("loading dataset")
   if type(dataset)!=type(None):
        print("Dataset already loaded")
        return dataset
   datetime_now = datetime.now().strftime("%B_%d_%Y")
   output_path = OOT_DIR+"/../datadump_{}.csv".format(datetime_now)
   print("dataset finish loading")
   return pd.read_csv(output_path)

def process_to_save_dataset():
    print("processing dataset")
    dataset = load_data_file()
    dataset = max_num_items(dataset)
    dataset = max_revenue(dataset)
    dataset = total_revenue(dataset)
    dataset = total_orders(dataset)
    dataset = day_since_last_order(dataset)
    dataset = two_consecutive_order(dataset)
    datetime_now = datetime.now().strftime("%B_%d_%Y")
    output_path = OOT_DIR+"/../datadump_{}.csv".format(datetime_now)
    dataset.to_csv(output_path, sep=",")
    print("finish processing dataset")
    return dataset 


def get_row_from_data(dataset, customer_id):
    row = dataset.loc[dataset['customer_id']==customer_id]
    row = row[['num_items_sum','revenue_max','revenue_total','order_id_total', 'day_since_last_order', 'gap_days']].values
    return row


async def calculate_customer_clv(dataset, model, customer_id):
   print(" get data ")
   row_arrays = get_row_from_data(dataset, customer_id)
#   result = model.predict(row_arrays)
   result = 10
   return result

model = None
dataset = None
def start():
    print("loading model and dataset")
    global model
    global dataset
    model = load_model(model)
    dataset = load_dataset(dataset)


@app.route("/get_clv")
async def get_clv(request):
    global model
    global dataset
    body = request.json
    customer_id = body['customer_id']
    try:
        clv = await calculate_customer_clv(dataset, model, customer_id)
    except Exception as exc:
        raise failcsv(_message=exc.args)
    return response.json({'clv':clv})


@app.route("/refresh_data")
async def refresh_data(request):
    global dataset
    dataset = None
    dataset = process_to_save_dataset(dataset)
    return response.json({'code':200, 'message': 'OK' })
#dataset = load_data_file()
#result = model.predict(dataset
start()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7787)

