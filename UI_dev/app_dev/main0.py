# https://doc.qt.io/qtforpython/tutorials/expenses/expenses.html#menu-bar

import sys
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget,  QMessageBox, QSizePolicy)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from six_bar import *


class plot_figure(FigureCanvas):

    def __init__(self, parent=None, width=50, height=50, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.m = My_mechanism(26,79,18,22,2)
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop, interval=10)
        self.draw()

    def animate_loop(self,i):
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


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        # Example data
        self._data = {"Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
                      "Supermarket": 230.4, "Internet": 29.99, "Bars": 21.85,
                      "Public transportation": 60.0, "Coffee": 22.45, "Restaurants": 120}

        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(2) # table columns
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Right
        self.description = QLineEdit()
        self.price = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")
        self.plot_figure = plot_figure(self, width=8, height=4)

        # Disabling 'Add' button
        self.add.setEnabled(False)

        self.right = QVBoxLayout()
        self.right.addWidget(self.plot_figure)
        self.right.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("Price"))
        self.right.addWidget(self.price)
        self.right.addWidget(self.add)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        # QWidget Layout
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Signals and pyqtSlots
        self.add.clicked.connect(self.add_element)
        self.quit.clicked.connect(self.quit_application)
        # self.plot.clicked.connect(self.plot_data)
        self.clear.clicked.connect(self.clear_table)
        self.description.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)

        # Fill example data
        self.fill_table()

    @pyqtSlot()
    def add_element(self):
        des = self.description.text()
        price = self.price.text()

        self.table.insertRow(self.items)
        description_item = QTableWidgetItem(des)
        price_item = QTableWidgetItem("{:.2f}".format(float(price)))
        price_item.setTextAlignment(Qt.AlignRight)

        self.table.setItem(self.items, 0, description_item)
        self.table.setItem(self.items, 1, price_item)

        self.description.setText("")
        self.price.setText("")

        self.items += 1

    @pyqtSlot()
    def check_disable(self):
        if not self.description.text() or not self.price.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

    # @pyqtSlot()
    # def plot_data(self):
    #     # Get table information
    #     series = QtCharts.QPieSeries()
    #     for i in range(self.table.rowCount()):
    #         text = self.table.item(i, 0).text()
    #         number = float(self.table.item(i, 1).text())
    #         series.append(text, number)
    #
    #     chart = QtCharts.QChart()
    #     chart.addSeries(series)
    #     chart.legend().setAlignment(Qt.AlignLeft)
    #     self.chart_view.setChart(chart)

    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, price in data.items():
            description_item = QTableWidgetItem(desc)
            price_item = QTableWidgetItem("{:.2f}".format(price))
            price_item.setTextAlignment(Qt.AlignRight)
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, price_item)
            self.items += 1

    @pyqtSlot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")

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
	window.show()
	# Execute application
	sys.exit(app.exec_())