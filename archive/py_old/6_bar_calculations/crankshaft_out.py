from crankshaft import *
from joblib import Parallel, delayed
import multiprocessing
import time

initial_time = time.time()
#a,b,p,q,omega 25,70,20,15
for a in range(290,300):
    for b in range(65,75):
        for p in range(15,25):
            for q in range(10,20):
                m = My_mechanism(a,b,p,q,2)
                try:
                    m.velocity_params()
                except Exception:
                    continue

print("Processing time : ",time.time()-initial_time,"s")
