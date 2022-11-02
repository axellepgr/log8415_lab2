#! /bin/bash
source ~/.bashrc
/usr/local/spark/bin/spark-submit pyspark_wordcount.py > experiment_spark_time.txt