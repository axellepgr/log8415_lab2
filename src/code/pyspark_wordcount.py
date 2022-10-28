import pyspark
import timeit
sc = pyspark.SparkContext('local[*]')

dataset1 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset2 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset3 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset4 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset5 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset6 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset7 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset8 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset9 = sc.textFile('').flatMap(lambda line: line.split(' '))



wordCounts1 = dataset1.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts2 = dataset2.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts3 = dataset3.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts4 = dataset4.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts5 = dataset5.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts6 = dataset6.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts7 = dataset7.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts8 = dataset8.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
wordCounts9 = dataset9.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)