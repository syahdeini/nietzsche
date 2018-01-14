# nietzsche
CLV calculator build on top of sanic framework
port : 7787

# How this microprocess work
[I want to draw an image here]

inside **load model**:
load model from model/model.dll, and load it into memory

inside **load dataset**:
return dataset from memory, if it doesn't exist
return data from compiled csv from warehous/datadum_[Date].csv, if it doesn't exist
process raw csv data from data/orders.csv and compiled it into csv, save it, and load it to memory.

to refresh data in memory call /refresh_data

## Endpoint


### GET /get_clv
input as json 
```
{
   customer_id : [customer_id]
}
```
output 
```
{
 clv : [clv_value]
}
```
e.g
```
input
{
    'customer_id' : '450e1c2cbd21687780153995f1be0c23'

}
```
output
```
{
   clv: [​ ​244.9,​ ​ ​ ​89.9]
}
```


### /refresh_data

this endpoint will refresh the data by compiling new csv from our raw dataset.
It also save the new compiled data into memory so the process will not need to compiled or load the new csv anymore.


## how to run 

### Using Docker

First you need to build the docker file
```
cd nietszche
docker build -t [name of the docker image] .
docker run [name of the docker image]
```
e.g
```
cd nietszche
docker build -t spinoza .
docker run spinoza
```


### Without docker
```
python3 source/app.py
```

The data processor should be run frequently (e.g every 12.00 am) 
it can be run using cron job, but I prefer using airflow



## Benchmark
Benchmark is tested using wrk
the test machine information :
```
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                4
On-line CPU(s) list:   0-3
Thread(s) per core:    2
Core(s) per socket:    2
Socket(s):             1
NUMA node(s):          1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 78
Model name:            Intel(R) Core(TM) i5-6200U CPU @ 2.30GHz
Stepping:              3
CPU MHz:               799.951
CPU max MHz:           2800,0000
CPU min MHz:           400,0000
BogoMIPS:              4800.00
Virtualization:        VT-x
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              3072K
NUMA node0 CPU(s):     0-3
```
Baseline benchmark
```
wrk http://0.0.0.0:7787/get_clv -c 1 -t 1 -s benchmarks/scripts/benchmark.lua 
Running 10s test @ http://0.0.0.0:7787/get_clv
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    54.78ms    9.69ms  82.38ms   80.77%
    Req/Sec    18.19      3.86    20.00     82.00%
  182 requests in 10.01s, 43.37KB read
Requests/sec:     18.19
Transfer/sec:      4.33KB
```
100 connection with 8 threads
```
wrk http://0.0.0.0:7787/get_clv -c 100 -t 8  -s benchmarks/scripts/benchmark.lua 
Running 10s test @ http://0.0.0.0:7787/get_clv
  8 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.15s   443.04ms   1.67s    60.00%
    Req/Sec     3.36      4.13    14.00     90.91%
  126 requests in 10.10s, 30.02KB read
  Socket errors: connect 0, read 0, write 0, timeout 96
Requests/sec:     12.48
Transfer/sec:      2.97KB
```
1000 connection with 4 threads
```
wrk http://0.0.0.0:7787/get_clv -c 1000 -t 4  -s benchmarks/scripts/benchmark.lua 
Running 10s test @ http://0.0.0.0:7787/get_clv
  4 threads and 1000 connections

  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     0.00us    0.00us   0.00us    -nan%
    Req/Sec    18.00      0.00    18.00    100.00%
  160 requests in 10.07s, 38.12KB read
  Socket errors: connect 0, read 0, write 0, timeout 160
Requests/sec:     15.89
Transfer/sec:      3.79KB
```

## P.S 
The docker images can be deployed in kubernetes server 
it's better put prometheus_client on the microservice
and to use airflow as a scheduller for calculating new compiled csv
