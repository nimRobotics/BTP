import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["x-component", "y-component","z-component"])
        self.tableWidget.setVerticalHeaderLabels(["Description", "Price"])
        self.tableWidget.setItem(0,0, QTableWidgetItem("as"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Ceddll (1,2)"))
        self.tableWidget.setItem(0,2, QTableWidgetItem("Ceddll (1,2)"))
        # self.tableWidget.setItem(1,0, QTableWidgetItem("Cesll (2,1)"))
        # self.tableWidget.setItem(1,1, QTableWidgetItem("Ced2,2)"))
        # self.tableWidget.setItem(2,0, QTableWidgetItem("Ck,1)"))
        # self.tableWidget.setItem(2,1, QTableWidgetItem("Cen (3,2)"))
        # self.tableWidget.setItem(3,0, QTableWidgetItem(" (4,1)"))
        # self.tableWidget.setItem(3,1, QTableWidgetItem("Celdslkjk (4,2)"))
        self.tableWidget.move(0,0)

        # table selection change
        # self.tableWidget.doubleClicked.connect(self.on_click)

        # self.fill_table()

    # @pyqtSlot()
    # def add_element(self):
    #     des = "HI"
    #     price = 10

    #     self.tableWidget.insertRow(self.items)
    #     description_item = QTableWidgetItem(des)
    #     price_item = QTableWidgetItem("{:.2f}".format(float(price)))
    #     price_item.setTextAlignment(Qt.AlignRight)

    #     self.tableWidget.setItem(self.items, 0, description_item)
    #     self.tableWidget.setItem(self.items, 1, price_item)

    #     self.description.setText("")
    #     self.price.setText("")

    #     self.items += 1
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  
