"""
@nimrobotics

# https://doc.qt.io/qtforpython/tutorials/expenses/expenses.html#menu-bar

TODO:
dark theme: https://stackoverflow.com/questions/48256772/dark-theme-for-qt-widgets
screen shot: https://stackoverflow.com/questions/51361674/is-there-a-way-to-take-screenshot-of-a-window-in-pyqt5-or-qt5
autoscroll velocity plot
add margins
autoscale plots         self.ax1.set_autoscale_on(True)


# BUG:
lenght of link a various in slider crank mechanism

"""

import sys
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QRadioButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget,  QMessageBox, QSizePolicy)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mechanismClass import *


class plot_figure(FigureCanvas):

    def __init__(self, width=50, height=50, dpi=100, parent=None,):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def draw_graph_fourbar(self, a, b, p, q, omega):
        self.ax1 = self.fig.add_subplot(2,1,1)
        # self.ax2 = self.fig.add_subplot(2,1,2)
        self.m = My_mechanism(a,b,p,q,omega)
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop_fourbar, interval=10)
        self.draw()

    def animate_loop_fourbar(self,i):
        p_x,p_y = self.m.rod_p_position(self.m.k)
        q_x,q_y = self.m.rod_q_position(self.m.k)
        # c_x = self.m.piston_position(self.m.k)
        self.ax1.clear()
        # self.ax2.clear()
        # rod P
        self.ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
        # rod Q
        self.ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
        # rod A
        self.ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
        # rod B
        # self.ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
        # Piston (c)
        # self.ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')
        self.ax1.set_xlim(-50,50)
        self.ax1.set_ylim(-50,50)
        self.ax1.set_title('Crankshaft, connecting rod and piston mechanism')
        # Piston speed
        # self.m.c_speed.append(self.m.c_dot(self.m.k))
        # self.m.c_time.append(100*self.m.k)
        # self.ax2.plot(self.m.c_time,self.m.c_speed,color='green')
        # self.ax2.set_xlim(0,600)
        # self.ax2.set_ylim(0,200)
        # self.ax2.set_ylabel("Speed $(m/s)$")
        # self.ax2.set_xlabel("time $(s*100)$")
        # self.ax2.set_title('Piston speed')
        self.ax1.set_aspect("equal")
        # self.ax2.set_aspect("equal")
        self.m.k += 0.01


    def draw_graph_sixbar(self, a, b, p, q, omega):
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        self.m = My_mechanism(a,b,p,q,omega)
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop_sixbar, interval=10)
        self.draw()

    def animate_loop_sixbar(self,i):
        p_x,p_y = self.m.rod_p_position(self.m.k)
        q_x,q_y = self.m.rod_q_position(self.m.k)
        c_x = self.m.piston_position(self.m.k)
        self.ax1.clear()
        self.ax2.clear()
        # rod P
        self.ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
        # rod Q
        self.ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
        # rod A
        self.ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
        # rod B
        self.ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
        # Piston (c)
        self.ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')
        self.ax1.set_xlim(-50,130)
        self.ax1.set_ylim(-50,50)
        self.ax1.set_title('Crankshaft, connecting rod and piston mechanism')
        # Piston speed
        self.m.c_speed.append(self.m.c_dot(self.m.k))
        self.m.c_time.append(100*self.m.k)
        self.ax2.plot(self.m.c_time,self.m.c_speed,color='green')
        self.ax2.set_xlim(0,600)
        self.ax2.set_ylim(0,200)
        self.ax2.set_ylabel("Speed $(m/s)$")
        self.ax2.set_xlabel("time $(s*100)$")
        self.ax2.set_title('Piston speed')
        self.ax1.set_aspect("equal")
        self.ax2.set_aspect("equal")
        self.m.k += 0.01


    def draw_graph_slider(self, a, b, omega):
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        self.m = My_mechanism_slider(a,b,omega)
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop_slider, interval=10)
        self.draw()

    def animate_loop_slider(self,i):
        # p_x,p_y = self.m.rod_p_position(self.m.k)
        a_x,a_y = self.m.rod_a_position(self.m.k)
        c_x = self.m.piston_position(self.m.k)
        self.ax1.clear()
        self.ax2.clear()
        # rod P
        # self.ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
        # rod Q
        # self.ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
        # rod A
        self.ax1.plot([a_x,link_a_pivot[0]],[a_y,link_a_pivot[1]],linewidth=3,color='red')
        # rod B
        self.ax1.plot([a_x,c_x],[a_y,link_a_pivot[1]],linewidth=3,color='yellow')
        # Piston (c)
        self.ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')
        self.ax1.set_xlim(-50,130)
        self.ax1.set_ylim(-50,50)
        self.ax1.set_title('Crankshaft, connecting rod and piston mechanism')
        # Piston speed
        self.m.c_speed.append(self.m.c_dot(self.m.k))
        self.m.c_time.append(100*self.m.k)
        # self.ax2.plot(self.m.c_time,self.m.c_time)
        self.ax2.plot(self.m.c_time,self.m.c_speed,color='green')
        self.ax2.set_xlim(0,600)
        self.ax2.set_ylim(0,200)
        self.ax2.set_ylabel("Speed $(m/s)$")
        self.ax2.set_xlabel("time $(s*100)$")
        self.ax2.set_title('Piston speed')
        self.ax1.set_aspect("equal")
        self.ax2.set_aspect("equal")
        self.m.k += 0.01


    def clear_plot(self, plots):
        self.anim.event_source.stop()
        if plots==1:
            self.ax1.clear()
            print("1")
        if plots==2:
            print("2")
            self.ax1.clear()
            self.ax2.clear()
        self.draw()


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.a=26
        self.b=76
        self.p=18
        self.q=22
        self.omega=2

        # Right
        # a=26,b=79,p=18,q=22,omega=2
        self.plot_figure = plot_figure(width=8, height=4)
        self.right = QVBoxLayout()
        self.right.addWidget(self.plot_figure)

        # Left: selectMechanism radio buttons
        self.fourbar = QRadioButton("Four bar")
        self.slidercrank = QRadioButton("Slider crank")
        self.sixbar = QRadioButton("Six bar")

        self.selectMechanism = QHBoxLayout()
        self.selectMechanism.addWidget(self.fourbar)
        self.selectMechanism.addWidget(self.slidercrank)
        self.selectMechanism.addWidget(self.sixbar)

        self.fourbar.setChecked(True)
        self.fourbar.toggled.connect(self.four_bar)
        self.slidercrank.toggled.connect(self.slider_crank)
        self.sixbar.toggled.connect(self.six_bar)

        # left: link lengths input
        self.lenA = QLineEdit()
        self.lenAbox = QHBoxLayout()
        self.lenAbox.addWidget(QLabel("Link A length"))
        self.lenAbox.addWidget(self.lenA)
        self.lenAbox.addWidget(QLabel("cm"))

        self.lenB = QLineEdit()
        self.lenB.setEnabled(False)
        self.lenBbox = QHBoxLayout()
        self.lenBbox.addWidget(QLabel("Link B length"))
        self.lenBbox.addWidget(self.lenB)
        self.lenBbox.addWidget(QLabel("cm"))

        self.lenP = QLineEdit()
        self.lenPbox = QHBoxLayout()
        self.lenPbox.addWidget(QLabel("Link P length"))
        self.lenPbox.addWidget(self.lenP)
        self.lenPbox.addWidget(QLabel("cm"))

        self.lenQ = QLineEdit()
        self.lenQbox = QHBoxLayout()
        self.lenQbox.addWidget(QLabel("Link Q length"))
        self.lenQbox.addWidget(self.lenQ)
        self.lenQbox.addWidget(QLabel("cm"))

        self.omega = QLineEdit()
        self.omegabox = QHBoxLayout()
        self.omegabox.addWidget(QLabel("Angular speed"))
        self.omegabox.addWidget(self.omega)
        self.omegabox.addWidget(QLabel("rad/s"))



        # left
        self.description = QLineEdit()
        self.price = QLineEdit()
        self.add = QPushButton("Simulate")
        # Disabling 'Add' button
        self.add.setEnabled(False)
        self.reset = QPushButton("Reset")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")

        self.left = QVBoxLayout()
        self.left.addWidget(QLabel("Select the mechanism"))
        self.left.addLayout(self.selectMechanism)
        self.left.addWidget(QLabel("Specify the mechanism params"))
        self.left.addLayout(self.lenAbox)
        self.left.addLayout(self.lenBbox)
        self.left.addLayout(self.lenPbox)
        self.left.addLayout(self.lenQbox)
        self.left.addLayout(self.omegabox)
        self.left.addWidget(self.add)
        self.left.addWidget(self.reset)
        self.left.addWidget(self.clear)
        self.left.addWidget(self.quit)

        # Signals and pyqtSlots
        self.add.clicked.connect(self.add_element)
        self.quit.clicked.connect(self.quit_application)
        self.reset.clicked.connect(self.reset_values)
        self.clear.clicked.connect(self.clear_inputs)


        # check when to enable Simulate button
        self.lenA.textChanged[str].connect(self.check_disable)
        self.lenB.textChanged[str].connect(self.check_disable)
        self.lenP.textChanged[str].connect(self.check_disable)
        self.lenQ.textChanged[str].connect(self.check_disable)
        self.omega.textChanged[str].connect(self.check_disable)
        # self.fourbar.


        # QWidget Layout
        self.layout = QHBoxLayout()

        # self.layout.addWidget(self.table)
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)


    # onClick for fourbar radio
    @pyqtSlot()
    def four_bar(self):
        if self.sender().isChecked():
            self.lenP.setEnabled(True)
            self.lenQ.setEnabled(True)
            self.lenA.setEnabled(True)
            self.lenB.setEnabled(False)
        self.check_disable()

    # onClick for slidercrank radio
    @pyqtSlot()
    def slider_crank(self):
        if self.sender().isChecked():
            self.lenP.setEnabled(False)
            self.lenQ.setEnabled(False)
            self.lenA.setEnabled(True)
            self.lenB.setEnabled(True)
        self.check_disable()

    # onClick for sixbar radio
    @pyqtSlot()
    def six_bar(self):
        if self.sender().isChecked():
            self.lenP.setEnabled(True)
            self.lenQ.setEnabled(True)
            self.lenA.setEnabled(True)
            self.lenB.setEnabled(True)
        self.check_disable()

    @pyqtSlot()
    def add_element(self):
        if self.fourbar.isChecked():
            self.plot_figure.draw_graph_fourbar(int(self.lenA.text()), 0,
                                        int(self.lenP.text()), int(self.lenQ.text()), int(self.omega.text()))
            print(self.lenA.text(),self.lenP.text(),self.lenQ.text(),self.omega.text())

        if self.slidercrank.isChecked():
            self.plot_figure.draw_graph_slider(int(self.lenA.text()), int(self.lenB.text()),int(self.omega.text()))
            print(self.lenA.text(),self.lenB.text(),self.omega.text())

        if self.sixbar.isChecked():
            self.plot_figure.draw_graph_sixbar(int(self.lenA.text()), int(self.lenB.text()),
                                        int(self.lenP.text()), int(self.lenQ.text()), int(self.omega.text()))
            print(self.lenA.text(),self.lenB.text(),self.lenP.text(),self.lenQ.text(),self.omega.text())


    # enable add button after required inputs are met
    @pyqtSlot()
    def check_disable(self):
        if self.fourbar.isChecked():
            if not self.lenA.text() or not self.lenP.text() or not self.lenQ.text() or not self.omega.text():
                self.add.setEnabled(False)
            else:
                self.add.setEnabled(True)

        if self.slidercrank.isChecked():
            if not self.lenA.text() or not self.lenB.text() or not self.omega.text():
                self.add.setEnabled(False)
            else:
                self.add.setEnabled(True)

        if self.sixbar.isChecked():
            if not self.lenA.text() or not self.lenB.text() or not self.lenP.text() or not self.lenQ.text() or not self.omega.text():
                self.add.setEnabled(False)
            else:
                self.add.setEnabled(True)

    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    # sets the default values i.e.six bar constant velocity
    @pyqtSlot()
    def reset_values(self):
        # a=26,b=79,p=18,q=22,omega=2
        self.lenA.setText("26")
        self.lenB.setText("79")
        self.lenP.setText("18")
        self.lenQ.setText("22")
        self.omega.setText("2")
        self.sixbar.setChecked(True)

    # clears all input fields
    @pyqtSlot()
    def clear_inputs(self):
        self.lenA.setText("")
        self.lenB.setText("")
        self.lenP.setText("")
        self.lenQ.setText("")
        self.omega.setText("")

        if self.fourbar.isChecked():
            self.plot_figure.clear_plot(1)
        else:
            self.plot_figure.clear_plot(2)

        self.fourbar.setChecked(True)




class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("OpenKDM")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        self.setCentralWidget(widget)

    @pyqtSlot()
    def exit_app(self):
        QApplication.quit()


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(800, 600)
    # to set custom size
    # window.show()
    # to use the full available screen
    # window.showFullScreen()
    window.showMaximized()
    # Execute Application
    sys.exit(app.exec_())
