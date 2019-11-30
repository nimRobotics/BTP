# http://firsttimeprogrammer.blogspot.com/2015/02/crankshaft-connecting-rod-and-piston.html

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve
import numpy as np
import time
import math

plt.style.use('ggplot')
link_a_pivot = (0,-10)
link_p_pivot = (0,0)
x, y, h = symbols('x y h')

class My_mechanism(object):

    # The init function
    def __init__(self,a,b,p,q,omega):
        self.a = a                            # Rod a
        self.b = b                            # Rod b
        self.p = p                            # Rod p
        self.q = q                            # Rod q
        self.omega = omega            # Angular speed of rod a in rad/s
        self.theta0 = 0                  # Initial angular position of rod a
        self.set0 = (0,-100)
        self.k = np.array([0.001])             # Initial time for animation
        self.c_position = []                  # Piston position for animation
        self.conn_rod_angular_speed = []      # Classes for the graphs animation
        self.c_speed = []
        self.pos_old = 0

    # Angular position of rod a as a function of time
    def theta(self,t):
        if not all(t):
            raise ValueError('Each time t must be greater than 0')
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

        px,py = self.rod_p_position(t)
        ax,ay = link_a_pivot
        c = ((self.p**2-px**2-py**2) - (self.a**2-ax**2-ay**2)) / (2*(ax-px))
        d = (py-ay)/(ax-px)
        D = (d*(px-c)+py)**2 - (1+d**2)*(py**2 + (px-c)**2 - self.p**2)
        if D<0:
            print("complex")
            # raise Exception('complex')
        D2 = D**0.5
        y0 = (d*(px-c)+py+D2)/(1+d**2)
        y1 = (d*(px-c)+py-D2)/(1+d**2)
        x0 = c+d*y0
        x1 = c+d*y1
        set1=(x0,y0)
        set2=(x1,y1)
        # print(set1,set2)

        try:
            dist1 = math.hypot(set1[0] - self.set0[0], set1[1] - self.set0[1])
            dist2 = math.hypot(set2[0] - self.set0[0], set2[1] - self.set0[1])
            if dist1<dist2:
                self.set0=set1
                return set1[0],set1[1]
            else:
                self.set0=set2
                return set2[0],set2[1]
        except TypeError as e:
            print(e)

    def piston_position(self,t):
        initial_time = time.time()
        q_x,q_y = self.rod_q_position(t)
        print("qpos",time.time()-initial_time)
        initial_time = time.time()
        # eq3= (q_x-h)**2 + (q_y-link_a_pivot[1])**2 - self.b**2
        # set2 =solve(eq3,h)[1]
        h0 = q_x+(self.b**2 - (q_y-link_a_pivot[1])**2)**0.5
        # print("gh",h0)
        # print(set2)
        print("ppos",time.time()-initial_time)
        return h0

    # Piston speed
    def c_dot(self,t):
        c_x = self.piston_position(t)
        # c_dot = (c_x-self.pos_old)/0.05
        c_dot = abs(c_x-self.pos_old)/0.01
        self.pos_old = c_x
        return c_dot

    # Animation using matplotlib
    def animation_m(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        def animate(i):
            # a_x,a_y = self.rod_a_position(self.k)
            p_x,p_y = self.rod_p_position(self.k)
            q_x,q_y = self.rod_q_position(self.k)
            # print(q_x,q_y)
            c_x = self.piston_position(self.k)
            ax1.clear()
            # Connecting rod (b)
            plt.xlim(-35,70)
            plt.ylim(-35,35)
            # rod P
            ax1.plot([link_p_pivot[0],p_x[0]],[link_p_pivot[1],p_y[0]],linewidth=3,color='blue')
            # rod Q
            ax1.plot([p_x[0],q_x],[p_y[0],q_y],linewidth=3,color='green')
            # rod A
            ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
            # # ax1.plot([0,a_x[0]],[0,a_y[0]],linewidth=3,color='blue')
            # # # Crankshaft rod (a)
            ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
            # Piston (c)
            # ax1.plot([link_a_pivot[0],c_x],[link_a_pivot[1],c_y],'o',markersize=20,color='magenta')
            plt.gca().set_aspect('equal', adjustable='box')

            self.k += 0.01

        # k is the time step, while the interval is the speed for showing the animation
        ani = animation.FuncAnimation(fig,animate,interval=10)
        plt.show()

    # Matplotlib animation with graphs
    def animation_m_plus(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        ax2 = fig.add_subplot(2,1,2)
        # ax3 = fig.add_subplot(3,1,3)

        def animate(i):
            p_x,p_y = self.rod_p_position(self.k)
            q_x,q_y = self.rod_q_position(self.k)
            c_x = self.piston_position(self.k)
            ax1.clear()
            ax2.clear()

            # rod P
            ax1.plot([link_p_pivot[0],p_x[0]],[link_p_pivot[1],p_y[0]],linewidth=3,color='blue')
            # rod Q
            ax1.plot([p_x[0],q_x],[p_y[0],q_y],linewidth=3,color='green')
            # rod A
            ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
            # rod B
            ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
            # Piston (c)
            # ax1.plot([link_a_pivot[0],c_x],[link_a_pivot[1],c_y],'o',markersize=20,color='magenta')

            ax1.set_xlim(-30,30)
            ax1.set_ylim(-30,30)
            ax1.set_title('Crankshaft, connecting rod and piston mechanism')

            # Piston speed
            self.c_speed.append(self.c_dot(self.k))
            ax2.plot(self.c_speed,color='green')
            ax2.plot([0,600],[0,0],linewidth=1,color='black')
            ax2.set_xlim(0,600)
            ax2.set_ylim(0,100)
            ax2.set_title('Piston speed')

            plt.gca().set_aspect('equal', adjustable='box')

            self.k += 0.01

        ani = animation.FuncAnimation(fig,animate,interval=10)
        plt.show()
