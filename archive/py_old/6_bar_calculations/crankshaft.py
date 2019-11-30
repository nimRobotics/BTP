# http://firsttimeprogrammer.blogspot.com/2015/02/crankshaft-connecting-rod-and-piston.html

# import matplotlib.animation as animation
# import matplotlib.pyplot as plt
# from sympy import symbols, Eq, solve
import numpy as np
import time
import math
import csv

# plt.style.use('ggplot')
link_a_pivot = (0,-10)
link_p_pivot = (0,0)
# x, y, h = symbols('x y h')

class My_mechanism(object):

    # The init function
    def __init__(self,a,b,p,q,omega):
        self.a = a                            # Rod a
        self.b = b                            # Rod b
        self.p = p                            # Rod p
        self.q = q                            # Rod q
        self.omega = omega            # Angular speed of rod a in rad/s
        self.theta0 = 0               # Initial angular position of rod a theta()
        self.set0 = (0,-100)          # for selecting one of the two solutions
        self.k = 0.0001               # Initial time for animation
        self.c_position = []          # Piston position for animation
        self.c_speed = []             # storing piston speed
        self.c_time = []              # storing the time intervals
        self.pos_old = 0  # old position of the piston for c_dot calculation

    # Angular position of rod a as a function of time
    def theta(self,t):
        # if not all(t):
        #     raise ValueError('Each time t must be greater than 0')
        theta = self.theta0 + self.omega*t
        return theta

    def rod_p_position(self,t):
        p_y = self.p*np.sin(self.theta(t))
        p_x = self.p*np.cos(self.theta(t))
        return p_x,p_y

    def rod_q_position(self,t):
        # eq1= (x-self.rod_p_position(t)[0])**2 + (y-self.rod_p_position(t)[1])**2 - self.p**2
        # eq2= (x-link_a_pivot[0])**2 + (y-link_a_pivot[1])**2 - self.a**2
        # set1,set2= solve((eq1,eq2), (x, y))
        # # dist = math.hypot(x2 - x1, y2 - y1)
        # # print(set1,set2)
        # # print(set1[0].is_real)
        px,py = self.rod_p_position(t)
        ax,ay = link_a_pivot
        c = ((self.p**2-px**2-py**2) - (self.a**2-ax**2-ay**2)) / (2*(ax-px))
        d = (py-ay)/(ax-px)
        D = (d*(px-c)+py)**2 - (1+d**2)*(py**2 + (px-c)**2 - self.p**2)
        if D<0:
            print("complex")
            raise Exception('complex')
        D2 = ( (d*(px-c)+py)**2 - (1+d**2)*(py**2 + (px-c)**2 - self.p**2)   )**0.5
        y0 = (d*(px-c)+py+D2)/(1+d**2)
        y1 = (d*(px-c)+py-D2)/(1+d**2)
        x0 = c+d*y0
        x1 = c+d*y1
        set1=(x0,y0)
        set2=(x1,y1)
        # print(set1,set2)

        dist1 = math.hypot(set1[0] - self.set0[0], set1[1] - self.set0[1])
        dist2 = math.hypot(set2[0] - self.set0[0], set2[1] - self.set0[1])
        if dist1<dist2:
            self.set0=set1
            return set1[0],set1[1]
        else:
            self.set0=set2
            return set2[0],set2[1]


    def piston_position(self,t):
        q_x,q_y = self.rod_q_position(t)
        # eq3= (q_x-h)**2 + (q_y-link_a_pivot[1])**2 - self.b**2
        # set2 =solve(eq3,h)[1]
        h0 = q_x+(self.b**2 - (q_y-link_a_pivot[1])**2)**0.5
        # print(h0)
        return h0

    # Piston speed
    def c_dot(self,t):
        c_x = self.piston_position(t)
        # c_dot = (c_x-self.pos_old)/0.05
        c_dot = abs(c_x-self.pos_old)/0.01  # dt = 0.01
        self.pos_old = c_x
        return c_dot

    def velocity_params(self):
        while self.k<3.2: # to get one complete cycle
            speed = self.c_dot(self.k)
            self.k+=0.01
            if self.k>0.3 and self.k<2.2:# store the ROI
                self.c_speed.append(speed)
                self.c_time.append(self.k)

        # print(self.c_speed)
        maxi = []
        mini = []
        for i in range(1,len(self.c_speed)-1):
            # local maxima
            if self.c_speed[i]>self.c_speed[i+1] and self.c_speed[i]>self.c_speed[i-1]:
                maxi.append(self.c_speed[i])
                # print("max",self.c_speed[i])
            # local minima
            if self.c_speed[i]<self.c_speed[i+1] and self.c_speed[i]<self.c_speed[i-1]:
                mini.append(self.c_speed[i])
                # print("min",self.c_speed[i])
        # print(self.a,self.b,self.p,self.q,max(maxi),min(mini))
        with open('data.csv', mode='a') as label_file:
           label_writer = csv.writer(label_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           label_writer.writerow([self.a,self.b,self.p,self.q,max(maxi),min(mini)])
