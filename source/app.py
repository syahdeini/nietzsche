import dill

import os
import sys
import dill
from numpy import genfromtxt

#sys.path.insert(0,os.path.join(os.path.abspath(__file__), '..',"model"))
#sys.path.append("/home/bukalapak/nietzsche/model")
#print(sys.path)

def load_model(path="../model/model.dill"):
    #print("loading model "+path)
    with open(path, 'rb') as f:
        model = dill.load(f)
        return model

def load_data_file(path="../data/orders.csv"):
    return genfromtxt(path, delimiter=',',dtype=str,skip_header=1)
    


model = load_model()
dataset = load_data_file()
#result = model.predict(dataset
import pdb; pdb.set_trace()

