#!/usr/bin/bash

export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="lab --no-browser --port=8888"

# local mode
#pyspark --driver-memory 7G

# standalone cluster
pyspark --master yarn \
   --driver-memory 3500M \
   --driver-cores 4 \
   --executor-memory 3500M \
   --executor-cores 4 \
   --num-executors 16 \
   --total-executor-cores 40
