# nietzsche
CLV calculator build on top of sanic framework
port : 7787

endpoint
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

this endpoint will refresh the data
(because the compiled data for calculating clv only load and calculate once, then the data is saved into variable (memory))
This end point will be called by scheduller


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
wrk http://0.0.0.0:7787/get_clv -c 10 -t 4 -s benchmarks/scripts/benchmark.lua 
Running 10s test @ http://0.0.0.0:7787/get_clv
  4 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   209.73ms   35.53ms 343.62ms   82.01%
    Req/Sec     6.97      3.14    20.00     88.61%
  194 requests in 10.02s, 23.37KB read
  Socket errors: connect 0, read 0, write 0, timeout 5
  Non-2xx or 3xx responses: 4
Requests/sec:     19.37
Transfer/sec:      2.33KB
```
1000 connection with 4 thread
```
wrk http://0.0.0.0:7787/get_clv -c 1000 -t 4  -s benchmarks/scripts/benchmark.lua 
Running 10s test @ http://0.0.0.0:7787/get_clv
  4 threads and 1000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.94s   264.94us   1.94s    68.97%
    Req/Sec    21.00      9.90    28.00    100.00%
  92 requests in 10.08s, 10.78KB read
  Socket errors: connect 0, read 0, write 0, timeout 63
Requests/sec:      9.13
Transfer/sec:      1.07KB
```

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

The docker images can be deployed in kubernetes server 
and the metrics from /metrics can be monitor using grafana

### Without docker
```
python3 source/app.py
```

The data processor should be run frequently (e.g every 12.00 am) 
it can be run using cron job, but I prefer using airflow

## Problem and next to do
problem that happen is, after first deploy
it will take more than 
Need to implement unittest
