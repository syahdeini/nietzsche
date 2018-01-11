#!/bin/sh
gunicorn --pythonpath=./source app:app --bind 0.0.0.0:7787 --worker-class sanic.worker.GunicornWorker -w 1 --timeout 120

