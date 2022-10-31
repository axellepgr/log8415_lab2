import os
import time

start = time.time()
os.system('cat pg4300.txt | tr " " "\n" | sort | uniq -c')
end = time.time()

print("total time: " + str(end - start))
