# this file configures the environment
export PATH=$PATH:/usr/local/spark/bin
export SPARK_LOCAL_IP=localhost
export PYSPARK_PYTHON=/usr/bin/python3
export PYTHONPATH=$(ZIPS=("$SPARK_HOME"/python/lib/*.zip); IFS=:; echo "${ZIPS[*]}"):$PYTHONPATH