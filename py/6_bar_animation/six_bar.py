"""
Contains main class for calculating and visualizing the mechanism

@nimrobotics
"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve
import numpy as np
import time
import math

plt.style.use('ggplot')

# ground for link a and p
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
        self.omega = omega                    # Angular speed of rod a in rad/s
        self.theta0 = 0                       # Initial angular position of rod a
        self.set0 = (0,-100)                  # for selecting one of the two solutions
        self.k=0                              # Initial time for animation
        self.c_position = []                  # Piston position for animation
        self.conn_rod_angular_speed = []      # Classes for the graphs animation
        self.c_speed = []                     # storing piston speed
        self.c_time = []                      # storing the time intervals
        self.pos_old = 0                      # old position of the piston for c_dot calculation

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

    # Animation using matplotlib
    def animation_m(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        def animate():
            # get the position values
            p_x,p_y = self.rod_p_position(self.k)
            q_x,q_y = self.rod_q_position(self.k)
            c_x = self.piston_position(self.k)

            ax1.clear()
            plt.xlim(-35,100)
            plt.ylim(-35,35)

            # rod P
            ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
            # rod Q
            ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
            # rod A
            ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
            # Crankshaft rod (a)
            ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
            # Piston (c)
            ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')

            plt.gca().set_aspect('equal', adjustable='box')

            self.k += 0.01

        # k is the time step, while the interval is time in ms for each frame
        ani = animation.FuncAnimation(fig,animate,interval=30)
        plt.show()

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
                ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
                # rod Q
                ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
                # rod A
                ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
                # rod B
                ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
                # Piston (c)
                ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')

                ax1.set_xlim(-50,130)
                ax1.set_ylim(-50,50)
                ax1.set_title('Crankshaft, connecting rod and piston mechanism')

                # Piston speed
                self.c_speed.append(self.c_dot(self.k))
                self.c_time.append(100*self.k)
                ax2.plot(self.c_time,self.c_speed,color='green')
                ax2.set_xlim(0,600)
                ax2.set_ylim(0,200)
                ax2.set_ylabel("Speed $(m/s)$")
                ax2.set_xlabel("time $(s*100)$")
                ax2.set_title('Piston speed')

                # plt.gca().set_aspect('equal', adjustable='box')
                ax1.set_aspect("equal")
                ax2.set_aspect("equal")
                # ax1.set_aspect(1./ax1.get_data_ratio())
                # ax2.set_aspect(1./ax2.get_data_ratio())
                # ax1.axis('square')

                self.k += 0.01

            ani = animation.FuncAnimation(fig,animate,interval=30)
            plt.show()
