from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class UiForm(QWidget):
    def __init__(self):
        super(UiForm, self).__init__()
        self.setWindowTitle('Ввод новых данных')
        self.setObjectName("form_2")
        self.resize(400, 218)
        self.user_reply = QtWidgets.QLineEdit(self)
        self.user_reply.setGeometry(QtCore.QRect(150, 150, 113, 22))
        self.user_reply.setObjectName("user_reply")
        self.text = QtWidgets.QLabel(self)
        self.text.setGeometry(QtCore.QRect(30, 40, 351, 71))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.text.setFont(font)
        self.text.setText("")
        self.text.setWordWrap(True)
        self.text.setObjectName("text")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(160, 180, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.user_reply.show()
        self.text.show()

    def user_reply_entered(self):
        pass

    def print_questions(self):
        pass
