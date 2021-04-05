import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
import MySQLdb as mdb


class Program(QtWidgets.QMainWindow):
    def __init__(self):
        super(Program, self).__init__()
        self.window = Ui_MainWindow()
        self.window.setupUi(self)

        self.table = Table(self.window)

        self.db = None
        # self.connect_base()

        tabs = ["Сотрудники", "Должности", "Отделы", "Имущество", "Поставщики", "Расположения", "Типы имущества"]
        for tab in tabs:
            temp = QtWidgets.QWidget()
            temp.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.window.tabWidget.addTab(temp, tab)

    def connect_base(self):
        self.db = mdb.connect('localhost', 'root', '321Ilyxazc', 'trpo_db')
        self.db.set_character_set("utf8")


class Table:
    def __init__(self, window):
        self.table = window.tableWidget

    def display_table(self, db, table_name):
        cursor = db.cursor()

        cursor.execute("SELECT * FROM {}".format(table_name))

        table = cursor.fetchall()

        self.table.tableWidget.setRowCount(0)
        self.table.tableWidget.setColumnCount(0)

        for row_number, row_data in enumerate(table):
            self.table.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if self.table.tableWidget.columnCount() <= column_number:
                    self.table.tableWidget.setColumnCount(self.table.tableWidget.columnCount() + 1)
                self.table.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

# QTabBar::tab:selected  {
#     background-color:rgb(255, 255, 0);
# }


# qss = '''
# QTabBar::tab {
#     background-color:rgb(220, 220, 0);
# }
# '''
app = QtWidgets.QApplication([])
# app.setStyleSheet(qss)
application = Program()
application.show()

sys.exit(app.exec())
