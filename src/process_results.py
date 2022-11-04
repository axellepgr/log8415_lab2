import matplotlib.pyplot as plt
import tarfile
from os import listdir
from os.path import isfile, join
import statistics
import numpy as np

def compare_linux_hadoop(file_linux, file_hadoop):
    '''
    This functions read the results file and compare them.
    file_linux : the result linux file to read
    file_hadoop : the result hadoop file to read
    '''
    real_linux = -1
    real_hadoop = -1
    with open(file_linux) as f:
        for line in f:
            data = line.strip()
            indice = data.find('0m')
            if (data[0] == 'r'): #real
                real_linux = float(data[indice+2:-1])
    f.close()
    with open(file_hadoop) as f:
        for line in f:
            data = line.strip()
            indice = data.find('0m')
            if (data[0] == 'r'): #real
                real_hadoop = float(data[indice+2:-1])
    f.close() 
    x = ['Hadoop', 'Linux']
    y = [real_hadoop, real_linux]
    plt.bar(x, y)
    plt.ylabel('Execution time (s)')
    plt.suptitle("Execution time for the file pg4300.txt")
    plt.savefig(f"results/graphs/hadoop_linux.png")
    plt.show()
    
def read_files(file_hadoop, file_spark):
    '''
    This functions read the files and prepare the datas.
    file_hadoop : the file to read
    file_spark : the file to read
    returns data_spark, data_hadoop, lists of float of the execution time
    '''
    data_spark = []
    data_hadoop = []
    with open(file_hadoop) as f:
        for line in f:
            data = line.strip()
            indice = data.find('0m')
            if (data[0] == 'r'): #real
                data_hadoop.append(float(data[indice+2:-1]))
    f.close()
    with open(file_spark) as f:
        for line in f:
            data = line.strip()
            data_spark.append(float(data))
    f.close()
    return data_spark, data_hadoop
    
def plot_graphs(data_hadoop, data_spark):
    '''
    This function plots the average execution time for both hadoop and sparl
    '''
    x = ['Hadoop', 'Spark']

    mean_real_hadoop = []
    mean_real_spark = data_spark
    i=0
    while i+3<=len(data_hadoop):
        mean_real_hadoop.append(statistics.mean(data_hadoop[i:i+3]))
        i+=3

    number_of_im = len(mean_real_hadoop)
    # Initialise the subplot function using number of rows and columns
    figure, axis = plt.subplots(3, 3)

    
    y1 = [mean_real_hadoop[0], mean_real_spark[0]*10]
    y2 = [mean_real_hadoop[1], mean_real_spark[1]*10]
    y3 = [mean_real_hadoop[2], mean_real_spark[2]*10]
    y4 = [mean_real_hadoop[3], mean_real_spark[3]*10]
    y5 = [mean_real_hadoop[4], mean_real_spark[4]*10]
    y6 = [mean_real_hadoop[5], mean_real_spark[5]*10]
    y7 = [mean_real_hadoop[6], mean_real_spark[6]*10]
    y8 = [mean_real_hadoop[7], mean_real_spark[7]*10]
    y9 = [mean_real_hadoop[8], mean_real_spark[8]*10]
    
    # For 1st file
    bar_colors = ['tab:blue', 'tab:orange']
    axis[0, 0].bar(x, y1, color=bar_colors)
    #plt.ylabel('average time (s)')
    axis[0, 0].set_title("file1")
    
    # For 2nd file
    axis[0, 1].bar(x, y2, color=bar_colors)
    axis[0, 1].set_title("file2")
    
    # For 3rd file
    axis[0, 2].bar(x, y3, color=bar_colors)
    axis[0, 2].set_title("file3")

    # For 4th file
    axis[1, 0].bar(x, y4, color=bar_colors)
    #plt.ylabel('average time (s)')
    axis[1, 0].set_title("file4")
 
    # For 5th file
    axis[1, 1].bar(x, y5, color=bar_colors)
    axis[1, 1].set_title("file5")
      
    # For 6th file
    axis[1, 2].bar(x, y6, color=bar_colors)
    axis[1, 2].set_title("file6")

    # For 7th file
    axis[2, 0].bar(x, y7, color=bar_colors)
    #plt.ylabel('average time (s)')
    axis[2, 0].set_title("file7")

    # For 8th file
    axis[2, 1].bar(x, y8, color=bar_colors)
    axis[2, 1].set_title("file8")

    # For 9th file
    axis[2, 2].bar(x, y9, color=bar_colors)
    axis[2, 2].set_title("file9")

    # Combine all the operations and display
    plt.suptitle("Average execution time for the 9 files.")
    plt.savefig(f"results/graphs/spark_hadoop.png")
    plt.tight_layout()
    plt.show()
    

compare_linux_hadoop("results/pg4300_linux_time.txt", "results/pg4300_hadoop_time.txt")
data_spark, data_hadoop = read_files("results/times.txt", "results/experiment_spark_time.txt")
plot_graphs(data_hadoop, data_spark)