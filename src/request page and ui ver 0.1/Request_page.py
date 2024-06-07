from PyQt5 import QtCore, QtGui, QtWidgets
from Patient_Dashboard import *
class Ui_Request_Form(object):
    def setupUi(self, Request_Form,doctor_name,clinic_name):
        print(doctor_name)
        Request_Form.setObjectName("Request_Form")
        Request_Form.resize(806, 436)

        self.doctorname_label = QtWidgets.QLabel(Request_Form)
        self.doctorname_label.setGeometry(QtCore.QRect(420, 50, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doctorname_label.setFont(font)
        self.doctorname_label.setObjectName("doctorname_label")

        self.doctorname_entry = QtWidgets.QLineEdit(Request_Form)
        self.doctorname_entry.setGeometry(QtCore.QRect(550, 50, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doctorname_entry.setFont(font)
        self.doctorname_entry.setReadOnly(True)
        self.doctorname_entry.setObjectName("doctorname_entry")
        self.doctorname_entry.setText(doctor_name)

        self.clinicname_entry = QtWidgets.QLineEdit(Request_Form)
        self.clinicname_entry.setGeometry(QtCore.QRect(130, 50, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clinicname_entry.setFont(font)
        self.clinicname_entry.setReadOnly(True)
        self.clinicname_entry.setObjectName("clinicname_entry")
        self.clinicname_entry.setText(clinic_name)

        self.clinicname_label = QtWidgets.QLabel(Request_Form)
        self.clinicname_label.setGeometry(QtCore.QRect(10, 50, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clinicname_label.setFont(font)
        self.clinicname_label.setObjectName("clinicname_label")

        self.confirm_label = QtWidgets.QLabel(Request_Form)
        self.confirm_label.setGeometry(QtCore.QRect(10, 10, 761, 31))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.confirm_label.setFont(font)
        self.confirm_label.setObjectName("confirm_label")

        self.requestreason_label = QtWidgets.QLabel(Request_Form)
        self.requestreason_label.setGeometry(QtCore.QRect(10, 100, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.requestreason_label.setFont(font)
        self.requestreason_label.setObjectName("requestreason_label")
        self.requestreason_edit = QtWidgets.QTextEdit(Request_Form)
        self.requestreason_edit.setGeometry(QtCore.QRect(10, 140, 781, 251))
        self.requestreason_edit.setObjectName("requestreason_edit")

        self.sendrequest_button = QtWidgets.QPushButton(Request_Form)
        self.sendrequest_button.setGeometry(QtCore.QRect(640, 400, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.sendrequest_button.setFont(font)
        self.sendrequest_button.setObjectName("sendrequest_button")

        self.retranslateUi(Request_Form)
        QtCore.QMetaObject.connectSlotsByName(Request_Form)

    def retranslateUi(self, Request_Form):
        _translate = QtCore.QCoreApplication.translate
        Request_Form.setWindowTitle(_translate("Request_Form", "Form"))
        self.doctorname_label.setText(_translate("Request_Form", "Doctor Name:"))
        self.clinicname_label.setText(_translate("Request_Form", "Clinic Name:"))
        self.confirm_label.setText(_translate("Request_Form", "Please kindly confirm the clinic name and doctor name before sending the request."))
        self.requestreason_label.setText(_translate("Request_Form", "Request Reason:"))
        self.sendrequest_button.setText(_translate("Request_Form", "Send"))

class Request_Page(QtWidgets.QWidget):
    def __init__(self,doctor_name,clinic_name):
        super().__init__()
        self.ui = Ui_Request_Form()
        self.ui.setupUi(self,doctor_name,clinic_name)


