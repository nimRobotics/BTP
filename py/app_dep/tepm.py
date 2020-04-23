from six_bar import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt

m = My_mechanism(26,79,18,22,2)
fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

def animate(i):
    print(i)
    # print(i)
    p_x,p_y = m.rod_p_position(m.k)
    q_x,q_y = m.rod_q_position(m.k)
    c_x = m.piston_position(m.k)
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
    m.c_speed.append(m.c_dot(m.k))
    m.c_time.append(100*m.k)
    ax2.plot(m.c_time,m.c_speed,color='green')
    ax2.set_xlim(0,600)
    ax2.set_ylim(0,200)
    ax2.set_ylabel("Speed $(m/s)$")
    ax2.set_xlabel("time $(s*100)$")
    ax2.set_title('Piston speed')

    # plt.gca().set_aspect('equal', adjustable='box')
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    m.k += 0.01
print('hello')
ani = animation.FuncAnimation(fig,animate,interval=5)
print('ads')
plt.show()
