# sum =0
# for i in range(10):
#     for j in range(10):
#         for k in range(10):
#             for l in range(10):
#                 sum=sum+1
# print(sum)


from crankshaft import *
import multiprocessing
import random
import time

initial_time = time.time()

p = multiprocessing.Pool(10)

for i in range(10,20):
    m = My_mechanism(i,50,20,14,2)
    try:
        p.apply_async(m.velocity_params())
    except Exception:
        continue

print("Processing time : ",time.time()-initial_time,"s")
