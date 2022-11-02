import pyspark
import timeit
import requests
import time
sc = pyspark.SparkContext('local[*]')

experiment_files = "./experiment_files.txt"


def load_experiment_files(experiment_files):
    with open(experiment_files, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
    return [x.strip() for x in raw_lines]


data = load_experiment_files(experiment_files)

for i in range(len(data)):
    # the lib that handles the url stuff
    r = requests.get(data[i], allow_redirects=True)
    open("text" + str(i) + ".txt", 'wb').write(r.content)
    words = sc.textFile("./text" + str(i) +
                        ".txt").flatMap(lambda line: line.split(' '))

    average_time = 0

    for j in range(3):
        start = time.time()
        map_reduce = words.map(lambda word: (
            word, 1)).reduceByKey(lambda a, b: a + b)
        end = time.time()
        average_time += end - start

    average_time = average_time / 3
    print(average_time)
