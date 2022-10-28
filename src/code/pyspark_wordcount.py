import pyspark
import timeit
sc = pyspark.SparkContext('local[*]')

experiment_files = "./experiment_files.txt"
def load_experiment_files(experiment_files):
    with open(experiment_files, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
    return [x.strip() for x in raw_lines]
data =load_experiment_files(experiment_files)

for i in range(9):
    dataset = sc.textFile(data[i]).flatMap(lambda line: line.split(' '))
    map_reduce = dataset.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    print( timeit.timeit(map_reduce, number=1))





'''
dataset1 = sc.textFile(data[0]).flatMap(lambda line: line.split(' '))
dataset2 = sc.textFile(data[0]).flatMap(lambda line: line.split(' '))
dataset3 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset4 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset5 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset6 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset7 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset8 = sc.textFile('').flatMap(lambda line: line.split(' '))
dataset9 = sc.textFile('').flatMap(lambda line: line.split(' '))



map_reduce_file1 = dataset1.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file2 = dataset2.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file3 = dataset3.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file4 = dataset4.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file5 = dataset5.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file6 = dataset6.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file7 = dataset7.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file8 = dataset8.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)
map_reduce_file9 = dataset9.map(lambda word: (word, 1)).reduceByKey(lambda a, b:a +b)

# Time calculation for each file
print("Time for file 1", timeit.timeit(map_reduce_file1, number=1))
print("Time for file 2", timeit.timeit(map_reduce_file2, number=1))
print("Time for file 3", timeit.timeit(map_reduce_file3, number=1))
print("Time for file 4", timeit.timeit(map_reduce_file4, number=1))
print("Time for file 5", timeit.timeit(map_reduce_file5, number=1))
print("Time for file 6", timeit.timeit(map_reduce_file6, number=1))
print("Time for file 7", timeit.timeit(map_reduce_file7, number=1))
print("Time for file 8", timeit.timeit(map_reduce_file8, number=1))
print("Time for file 9", timeit.timeit(map_reduce_file9, number=1))

'''