"""
this script carries out length_iterations for find the best constant velocity
curve and stores the data @ 'length_iterations.csv'

@nimrobotics
"""

from mechanism import *
import time

initial_time = time.time()

for a in range(20,35):
    for b in range(70,80):
        for p in range(15,25):
            for q in range(15,30):
                m = My_mechanism(a,b,p,q,2)     #a,b,p,q,omega
                try:
                    m.velocity_params(data_stored="iterations")
                except Exception:
                    continue

print("Processing time : ",time.time()-initial_time,"s")
