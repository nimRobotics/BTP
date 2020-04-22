"""
This script uses My_mechanism class to create the mechanism visualization
along with live velocity plot

@nimrobotics
"""

from six_bar import *

# (a,b,p,q,omega)
m = My_mechanism(26,79,18,22,2)

# plot only mechanism
# m.animation_m()

# plot mechanism with slider speed graph
m.animation_m_plus()
