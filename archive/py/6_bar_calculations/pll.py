from joblib import Parallel, delayed
import multiprocessing
import numpy

# what are your inputs, and what operation do you want to
# perform on each input. For example...
inputs = numpy.arange(0.001,3.5,0.01)
results = []
# print(inputs)

def processInput(i,j):
    return i * j,i+j
    # print()
    # results.append(i*j)

num_cores = multiprocessing.cpu_count()

results = Parallel(n_jobs=num_cores)(delayed(processInput)(i,10) for i in inputs)
list1, list2 = zip(*results)
print(list1)
