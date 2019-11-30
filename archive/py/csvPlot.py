import matplotlib.pyplot as plt
import numpy as np

x, y = np.loadtxt('dummy.csv', delimiter=',', unpack=True)
plt.plot(x,y, label='Loaded from file!')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Velocity Plot')
plt.legend()
plt.show()
