from crankshaft import *
import time

initial_time = time.time()
# m = My_mechanism(26,80,20,16,2)
# m = My_mechanism(20,65,15,10,2) # oneParam_old.csv
# m = My_mechanism(20,65,15,11,2) # oneParam_2.csv
# m = My_mechanism(26,74,18,19,2) # best
m = My_mechanism(26,79,18,22,2)   # best 2 26	79	18	22

m.velocity_params()
print("Processing time : ",time.time()-initial_time,"s")
