#! /bin/bash

# this file runs the Spark experiment
source ~/.bashrc
/usr/local/spark/bin/spark-submit pyspark_wordcount.py > experiment_spark_time.txt