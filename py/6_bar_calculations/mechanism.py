"""
Python class for six bar mechanism. Performs speed computations at various
time steps and stores data

@nimrobotics
"""

import numpy as np
import math
import csv

# ground for link a and p
link_a_pivot = (0,-10)
link_p_pivot = (0,0)

class My_mechanism(object):
    def __init__(self,a,b,p,q,omega):
        self.a = a                    # Rod a
        self.b = b                    # Rod b
        self.p = p                    # Rod p
        self.q = q                    # Rod q
        self.omega = omega            # Angular speed of rod a in rad/s
        self.theta0 = 0               # Initial angular position of rod a theta()
        self.set0 = (0,-100)          # for selecting one of the two solutions
        self.k = 0                    # Initial time for animation
        self.c_position = []          # Piston position for animation
        self.c_speed = []             # storing piston speed
        self.c_time = []              # storing the time intervals
        self.roi_speed=[]             # store roi speed
        self.roi_time=[]              # store roi time
        self.pos_old = 0              # old position of the piston for c_dot calculation

    # Angular position of rod a as a function of time
    def theta(self,t):
        theta = self.theta0 + self.omega*t
        return theta

    # position of end point of rod p
    def rod_p_position(self,t):
        p_y = self.p*np.sin(self.theta(t))
        p_x = self.p*np.cos(self.theta(t))
        return p_x,p_y

    # position of end point of rod q
    def rod_q_position(self,t):
        px,py = self.rod_p_position(t)
        ax,ay = link_a_pivot
        c = ((self.p**2-px**2-py**2) - (self.a**2-ax**2-ay**2)) / (2*(ax-px))
        d = (py-ay)/(ax-px)
        D = (d*(px-c)+py)**2 - (1+d**2)*(py**2 + (px-c)**2 - self.p**2)
        if D<0:
            """
            any length combination resulting in complex i.e. mechanism breaks
            will be skipped
            """
            raise Exception('complex')
        D2 = D**0.5
        y0 = (d*(px-c)+py+D2)/(1+d**2)
        y1 = (d*(px-c)+py-D2)/(1+d**2)
        x0 = c+d*y0
        x1 = c+d*y1
        set1=(x0,y0)
        set2=(x1,y1)

        dist1 = math.hypot(set1[0] - self.set0[0], set1[1] - self.set0[1])
        dist2 = math.hypot(set2[0] - self.set0[0], set2[1] - self.set0[1])
        if dist1<dist2:
            self.set0=set1
            return set1[0],set1[1]
        else:
            self.set0=set2
            return set2[0],set2[1]

    # position of piston end (i.e. slider)
    def piston_position(self,t):
        q_x,q_y = self.rod_q_position(t)
        h0 = q_x+(self.b**2 - (q_y-link_a_pivot[1])**2)**0.5
        return h0

    # Piston speed
    def c_dot(self,t):
        c_x = self.piston_position(t)
        c_dot = abs(c_x-self.pos_old)/0.01  # dt = 0.01
        self.pos_old = c_x
        return c_dot

    # stores and computes velocity data
    def velocity_params(self,data_stored):
        """
        Here the value time="3.5" is a hyperparameter. It denote the time taken
        for the mechanism to complete one cycle. To find it, first set it to some
        value say "10" and plot the slider speed vs time curve using 'slider_speed.csv'
        and note the time taken for one cycle from the curve
        """
        while self.k<3.5:
            speed = self.c_dot(self.k)

            self.c_speed.append(speed)
            self.c_time.append(self.k)

            # update time step
            self.k+=0.01

        # collect data (time,slider_speed) for a single set of params (lengths) using "slider_speed.py"
        if data_stored=="slider_speed":
            print("Computing time series data for slider speed")
            for itr in range(len(self.c_time)):
                with open('slider_speed.csv', mode='a') as label_file:
                   label_writer = csv.writer(label_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                   label_writer.writerow([self.c_time[itr],self.c_speed[itr]])


        elif data_stored=="iterations":
            print("Computing slider speed for various link length combinations")
            for itr in range(len(self.c_time)):
                # store the Region of Interest (RoI) i.e. plateau
                if self.c_time[itr]>0.4 and self.c_time[itr]<2.1:
                    self.roi_speed.append(self.c_speed[itr])
                    self.roi_time.append(self.c_time[itr])

            maxi = []
            mini = []

            for i in range(1,len(self.roi_speed)-1):

                # local maxima
                if self.roi_speed[i]>self.roi_speed[i+1] and self.roi_speed[i]>self.roi_speed[i-1]:
                    maxi.append(self.roi_speed[i])

                # local minima
                if self.roi_speed[i]<self.roi_speed[i+1] and self.roi_speed[i]<self.roi_speed[i-1]:
                    mini.append(self.roi_speed[i])

            with open('length_iterations.csv', mode='a') as label_file:
               label_writer = csv.writer(label_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
               label_writer.writerow([self.a,self.b,self.p,self.q,max(maxi),min(mini)])

            mini.clear()
            maxi.clear()
            self.c_speed.clear()
            self.k.clear()
            self.roi_speed.clear()
            self.roi_time.clear()
