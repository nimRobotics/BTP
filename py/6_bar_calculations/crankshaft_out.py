from crankshaft import *
import time

initial_time = time.time()
# #a,b,p,q,omega
# best
for a in range(20,35):
    for b in range(70,80):
        for p in range(15,25):
            for q in range(15,30):
                m = My_mechanism(a,b,p,q,2)
                try:
                    m.velocity_params()
                except Exception:
                    continue

print("Processing time : ",time.time()-initial_time,"s")
