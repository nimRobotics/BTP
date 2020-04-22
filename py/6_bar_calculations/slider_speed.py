"""
this script generates time series data for the slider speed
data stored @ slider_speed.csv

@nimrobotics
"""

from mechanism import *
import time

initial_time = time.time()
m = My_mechanism(26,79,18,22,2)

m.velocity_params(data_stored="slider_speed")
print("Processing time : ",time.time()-initial_time,"s")
