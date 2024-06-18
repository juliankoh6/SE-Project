from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QDate
from Patient_Dashboard import *
from PyQt5.QtWidgets import *

class Ui_Request_Form(object):
    def setupUi(self, Request_Form,doctor_name,clinic_name, patient_id ):
        def Send_request():
            doctor_name = self.doctorname_entry.text()
            clinic_name = self.clinicname_entry.text()
            request_reason = self.requestreason_edit.toPlainText()
            request_date = self.Request_dateEdit.date()

            current_datetime = QDateTime.currentDateTime()
            request_datetime = QDateTime(request_date, current_datetime.time())

            if request_datetime < current_datetime:
                self.msg_box_name = QMessageBox()
                self.msg_box_name.setText("You can't book a date that is already passed!")
                self.msg_box_name.setWindowTitle("Notification")
                self.msg_box_name.show()
            else:
                request_date = request_datetime.toString("yyyy-MM-dd")
                conn = sqlite3.connect('call_a_doctor.db')
                cursor = conn.cursor()

                cursor.execute('SELECT * FROM Clinic WHERE Clinic_Name = ?', (clinic_name,))
                find_clinic_id = cursor.fetchone()
                clinic_id = find_clinic_id[0]

                cursor.execute('SELECT * FROM Doctor WHERE Doctor_Name = ?', (doctor_name,))
                find_doctor_id = cursor.fetchone()
                doctor_id = find_doctor_id[0]

                print(doctor_id)
                print(clinic_id)
                print(request_date)
                print(patient_id)

                cursor.execute('SELECT * FROM Patient_Request WHERE Doctor_ID = ?', (doctor_id,))
                find_date = cursor.fetchall()
                sameDateOrNot = 0
                for items in find_date:
                    if request_date == items[5]:
                        sameDateOrNot = 1
                        break
                if sameDateOrNot == 0:
                    cursor.execute('SELECT * FROM Patient_Request WHERE Patient_ID = ?', (patient_id,))
                    find_date = cursor.fetchall()
                    samePersonDateOrNot = 0
                    for items in find_date:
                        if request_date == items[5]:
                            samePersonDateOrNot = 1
                            break
                    if samePersonDateOrNot == 0:
                        insert_command = '''
                                                                INSERT INTO Patient_Request (Patient_ID, Clinic_ID, Doctor_ID, 
                                                                Request_State, Request_Date, Request_Reason)
                                                                VALUES (?, ?, ?, ?, ?, ?)
                                                                '''
                        cursor.execute(insert_command,
                                       (patient_id, clinic_id, doctor_id, '0', request_date, request_reason))
                        conn.commit()
                        self.msg_box_name = QMessageBox()
                        self.msg_box_name.setText("Request Sent Successfully.")
                        self.msg_box_name.setWindowTitle("Notification")
                        self.msg_box_name.show()
                        Request_Form.close()
                    else:
                        self.msg_box_name = QMessageBox()
                        self.msg_box_name.setText("You have booked this date already!")
                        self.msg_box_name.setWindowTitle("Notification")
                        self.msg_box_name.show()
                else:
                    self.msg_box_name = QMessageBox()
                    self.msg_box_name.setText("This date has been requested.")
                    self.msg_box_name.setWindowTitle("Notification")
                    self.msg_box_name.show()
                conn.close()

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
        font.setPointSize(8)
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
        self.sendrequest_button.clicked.connect(Send_request)

        self.Request_dateEdit = QtWidgets.QDateEdit(Request_Form)
        self.Request_dateEdit.setGeometry(QtCore.QRect(550, 90, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.Request_dateEdit.setFont(font)
        self.Request_dateEdit.setObjectName("Request_dateEdit")
        self.Request_dateEdit.setDate(QDate.currentDate())

        self.Request_date_Label = QtWidgets.QLabel(Request_Form)
        self.Request_date_Label.setGeometry(QtCore.QRect(410, 90, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Request_date_Label.setFont(font)
        self.Request_date_Label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.Request_date_Label.setObjectName("Request_date_Label")

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
        self.Request_date_Label.setText(_translate("Request_Form", "Request Date:"))

class Request_Page(QtWidgets.QWidget):
    def __init__(self,doctor_name,clinic_name,patient_id):
        super().__init__()
        self.ui = Ui_Request_Form()
        self.ui.setupUi(self,doctor_name,clinic_name,patient_id)


