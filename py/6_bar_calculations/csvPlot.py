"""
Plot data from the csv file.

@nimrobotics
"""

import matplotlib.pyplot as plt
import numpy as np

# load data from csv
x, y = np.loadtxt('slider_speed.csv', delimiter=',', unpack=True)

# plot the data
plt.plot(x[1:]*100,y[1:])
plt.xlabel('Time $s*100$')
plt.ylabel('Speed $m/s$')
plt.title('Slider speed')
plt.show()
