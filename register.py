# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(279, 438)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, -30, 481, 631))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(80, 100, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(80, 190, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.enterLoginEdit = QtWidgets.QLineEdit(self.tab)
        self.enterLoginEdit.setGeometry(QtCore.QRect(80, 140, 113, 22))
        self.enterLoginEdit.setObjectName("enterLoginEdit")
        self.enterPassEdit = QtWidgets.QLineEdit(self.tab)
        self.enterPassEdit.setGeometry(QtCore.QRect(80, 220, 113, 22))
        self.enterPassEdit.setObjectName("enterPassEdit")
        self.enterEnterButton = QtWidgets.QPushButton(self.tab)
        self.enterEnterButton.setGeometry(QtCore.QRect(90, 290, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.enterEnterButton.setFont(font)
        self.enterEnterButton.setObjectName("enterEnterButton")
        self.enterGoToRegButton = QtWidgets.QPushButton(self.tab)
        self.enterGoToRegButton.setGeometry(QtCore.QRect(74, 330, 131, 28))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.enterGoToRegButton.setFont(font)
        self.enterGoToRegButton.setObjectName("enterGoToRegButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(60, 29, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(60, 89, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(60, 149, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(60, 289, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(60, 208, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.regLoginEdit = QtWidgets.QLineEdit(self.tab_2)
        self.regLoginEdit.setGeometry(QtCore.QRect(60, 60, 141, 22))
        self.regLoginEdit.setObjectName("regLoginEdit")
        self.regPassFEdit = QtWidgets.QLineEdit(self.tab_2)
        self.regPassFEdit.setGeometry(QtCore.QRect(60, 120, 141, 22))
        self.regPassFEdit.setObjectName("regPassFEdit")
        self.regPassSEdit = QtWidgets.QLineEdit(self.tab_2)
        self.regPassSEdit.setGeometry(QtCore.QRect(60, 180, 141, 22))
        self.regPassSEdit.setObjectName("regPassSEdit")
        self.regIdCB = QtWidgets.QComboBox(self.tab_2)
        self.regIdCB.setGeometry(QtCore.QRect(60, 240, 141, 22))
        self.regIdCB.setObjectName("regIdCB")
        self.regAdminRadioB = QtWidgets.QRadioButton(self.tab_2)
        self.regAdminRadioB.setGeometry(QtCore.QRect(60, 270, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.regAdminRadioB.setFont(font)
        self.regAdminRadioB.setObjectName("regAdminRadioB")
        self.regAdminPassEdit = QtWidgets.QLineEdit(self.tab_2)
        self.regAdminPassEdit.setGeometry(QtCore.QRect(60, 320, 151, 22))
        self.regAdminPassEdit.setObjectName("regAdminPassEdit")
        self.regRegisterButton = QtWidgets.QPushButton(self.tab_2)
        self.regRegisterButton.setGeometry(QtCore.QRect(60, 360, 151, 28))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.regRegisterButton.setFont(font)
        self.regRegisterButton.setObjectName("regRegisterButton")
        self.regReturnToEnterButton = QtWidgets.QPushButton(self.tab_2)
        self.regReturnToEnterButton.setGeometry(QtCore.QRect(60, 400, 151, 28))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.regReturnToEnterButton.setFont(font)
        self.regReturnToEnterButton.setObjectName("regReturnToEnterButton")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "????????"))
        self.label.setText(_translate("Form", "??????????"))
        self.label_2.setText(_translate("Form", "????????????"))
        self.enterEnterButton.setText(_translate("Form", "??????????"))
        self.enterGoToRegButton.setText(_translate("Form", "??????????????????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.label_3.setText(_translate("Form", "??????????"))
        self.label_4.setText(_translate("Form", "????????????"))
        self.label_5.setText(_translate("Form", "?????????????????? ????????????"))
        self.label_6.setText(_translate("Form", "???????????? ????????????????????????????"))
        self.label_7.setText(_translate("Form", "?????? ????????????????????"))
        self.regAdminRadioB.setText(_translate("Form", "??????????????????????????"))
        self.regRegisterButton.setText(_translate("Form", "????????????????????????????????????"))
        self.regReturnToEnterButton.setText(_translate("Form", "?????????????????? ???? ??????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
