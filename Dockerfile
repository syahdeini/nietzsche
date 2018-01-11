FROM alpine:edge

RUN apk update
RUN apk --no-cache add python3 libstdc++ libev gcc g++ python3-dev alpine-sdk 
RUN pip3 install --upgrade pip setuptools
    
RUN mkdir -p /application/source
RUN mkdir -p /application/model
RUN mkdir -p /application/warehouse
RUN mkdir -p /application/data

COPY entrypoint.sh /application
RUN chmod +x /application/entrypoint.sh
COPY source /application/source
COPY model /application/model
COPY data /application/data
COPY requirements.txt /application
COPY README.md /appication

WORKDIR /application
RUN pip3 install -r requirements.txt
