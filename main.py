import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
import MySQLdb as mdb


class Program(QtWidgets.QMainWindow):
    def __init__(self):
        super(Program, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = None
        self.cursor = None
        self.connect_base()
        self.print_table()

    def connect_base(self):
        self.db = mdb.connect('localhost', 'root', '321Ilyxazc', 'trpo_db')
        # try:
        #     db = mdb.connect('localhost', 'root', '321Ilyxazc', 'trpo_db')
        #     QMessageBox.about(self, 'Connection', 'Database Connected Successfully')
        #
        # except mdb.Error as e:
        #     QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
        #     sys.exit(1)

    def print_table(self):
        self.db = mdb.connect('localhost', 'root', '321Ilyxazc', 'trpo_db')
        self.db.set_character_set("utf8")

        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM Должности")

        table = cursor.fetchall()

        print(table)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)

        for row_number, row_data in enumerate(table):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if self.ui.tableWidget.columnCount() <= column_number:
                    self.ui.tableWidget.setColumnCount(self.ui.tableWidget.columnCount() + 1)
                self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


app = QtWidgets.QApplication([])
application = Program()
application.show()

sys.exit(app.exec())
