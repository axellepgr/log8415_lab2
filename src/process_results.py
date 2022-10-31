import matplotlib.pyplot as plt
import tarfile
from os import listdir
from os.path import isfile, join
import statistics

# list Hadoop results
files = [f for f in listdir("results/results/hadoop/") if isfile(join("results/results/hadoop/", f))]
FILES_HADOOP = [f'results/results/hadoop/{f}' for f in files]

# list Linux results
files = [f for f in listdir("results/results/linux/") if isfile(join("results/results/linux/", f))]
FILES_LINUX = [f'results/results/linux/{f}' for f in files]
  
def extract_files():
    '''
    This functions extracts the files from results.tar.gz
    '''
    # open file
    file = tarfile.open('results/results.tar.gz')
    # extracting file
    file.extractall('./results')
    file.close()

def read_file(file):
    '''
    This functions read the file.
    file : the file to read
    '''
    real = []
    user = []
    sys = []
    with open(file) as f:
        for line in f:
            data = line.strip()
            indice = data.find('0m')
            if (data[0] == 'r'): #real
                real.append(float(data[indice+2:-1]))
            elif (data[0] == 'u'): # user
                user.append(float(data[indice+2:-1]))
            elif (data[0] == 's'): #sys
                sys.append(float(data[indice+2:-1]))
    f.close()
    return [real, user, sys]
    
def plot_graphs(data_hadoop, data_linux):
    '''
    This function plots the average execution time for both hadoop and linux
    '''
    y = []
    x = ['Hadoop', 'Linux']

    mean_real_hadoop = []
    mean_user_hadoop = []
    mean_sys_hadoop = []
    mean_real_linux = []
    mean_user_linux = []
    mean_sys_linux = []
    for i in range(len(data_hadoop)):
        mean_real_hadoop.append(statistics.mean(data_hadoop[i][0]))
        mean_user_hadoop.append(statistics.mean(data_hadoop[i][1]))
        mean_sys_hadoop.append(statistics.mean(data_hadoop[i][2]))
        mean_real_linux.append(statistics.mean(data_linux[i][0]))
        mean_user_linux.append(statistics.mean(data_linux[i][1]))
        mean_sys_linux.append(statistics.mean(data_linux[i][2]))
    print(mean_real_hadoop)

    for i in range(len(mean_real_hadoop)):
        y = []
        y.append(mean_real_hadoop[i])
        y.append(mean_real_linux[i])
        plt.bar(x, y)
        plt.ylabel('average time (s)')
        plt.suptitle("Average execution time for file number  " + str(i+1))
        plt.savefig(f"results/${i}.png")
        plt.show()

data_hadoop = []
for file in (FILES_HADOOP):
    data_hadoop.append(read_file(file))
    
data_linux = []
for file in (FILES_LINUX):
    data_linux.append(read_file(file))
    
print(data_hadoop)
plot_graphs(data_hadoop, data_linux)