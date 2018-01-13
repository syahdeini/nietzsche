import os
import sys
import dill
from data_processor import *
from exceptions import FailClv,NoCustomerFound
from sanic.exceptions import RequestTimeout, NotFound
from sanic.response import json
from sanic import Sanic, response
import asyncio
import numpy
import coloredlogs, logging

logger = logging.getLogger(__name__)
#logger.propagate = False
coloredlogs.install(level='DEBUG')

app = Sanic()
loop = asyncio.get_event_loop()
OOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_csv_path():
  datetime_now = datetime.now().strftime("%B_%d_%Y")
  return OOT_DIR+"/../datadump_{}.csv".format(datetime_now)


def load_model(model, path=OOT_DIR+"/../model/model.dill"):
    if model:
        logger.info("model already loaded")
        return model
    logger.info("loading model "+path)
    try:
      with open(path, 'rb') as f:
          model = dill.load(f)
    except Exception as exc: 
      logger.error("Model not found at " + path)
    logger.info("finish load model")
    return model
    

def load_dataset(dataset):
   logger.info("loading dataset")
   if type(dataset)!=type(None):
        logger.info("Dataset already loaded")
        return dataset
        logger.info("dataset finish loading")
   try:
      return pd.read_csv(get_csv_path())
   except Exception as exc:
       if isinstance(exc,FileNotFoundError):
           logger.error("compiled csv file not found")
#           dataset = process_to_save_dataset()
           return process_to_save_dataset()
def process_to_save_dataset():
    logger.info("processing dataset")
    dataset = load_data_file()
    dataset = max_num_items(dataset)
    dataset = max_revenue(dataset)
    dataset = total_revenue(dataset)
    dataset = total_orders(dataset)
    dataset = day_since_last_order(dataset)
    dataset = two_consecutive_order(dataset)
    dataset.to_csv(get_csv_path(), sep=",")
    logger.info("finish processing dataset")
    return dataset 


def get_row_from_data(dataset, customer_id):
    row = dataset.loc[dataset['customer_id']==customer_id]
    row = row[['num_items_sum','revenue_max','revenue_total','order_id_total', 'day_since_last_order', 'gap_days']].values
    return row


async def calculate_customer_clv(dataset, model, customer_id):
   logger.info("getting data ... ")
   row_arrays = get_row_from_data(dataset, customer_id)
   if len(row_arrays)<1:
       raise NoCustomerFound
   logger.info("calculate clv ...")
   result = model.predict(row_arrays)
   return result

model = None
dataset = None
def start():
    logger.info("loading model and dataset")
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
        raise FailClv(_message=exc.args)
    return response.json({'customer_id':customer_id,'clv':clv})


@app.route("/refresh_data")
async def refresh_data(request):
    global dataset
    dataset = None
    dataset = process_to_save_dataset(dataset)
    return response.json({'code':200, 'message': 'OK' })

start()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7787)

