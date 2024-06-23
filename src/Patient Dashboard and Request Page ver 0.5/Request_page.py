from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QDate, QTime, Qt
from datetime import datetime, timedelta
from Patient_Dashboard import *
from PyQt5.QtWidgets import *
import sqlite3

class Ui_Request_Form(object):
    def setupUi(self, Request_Form,doctor_name,clinic_name, patient_id):
        def Send_request():
            doctor_name = self.doctorname_entry.text()
            clinic_name = self.clinicname_entry.text()
            request_reason = self.requestreason_edit.toPlainText()
            request_time = self.Request_dateEdit.time()
            current_time = QTime.currentTime()
            after_two_hours = current_time.addSecs(2 * 60 * 60)

            current_date = QDate.currentDate()
            request_date = self.Request_dateEdit.date()
            after_six_months = current_date.addMonths(6)

            eight_am = QTime(8, 0, 0)
            six_pm = QTime(18, 0, 0)

            if request_reason == "":
                self.msg_box_name = QMessageBox()
                self.msg_box_name.setText("You haven't write any reason yet!")
                self.msg_box_name.setWindowTitle("Notification")
                self.msg_box_name.show()
            elif request_time < eight_am or request_time > six_pm:
                self.msg_box_name = QMessageBox()
                self.msg_box_name.setText("This time is too late/early that not available for booking!")
                self.msg_box_name.setWindowTitle("Notification")
                self.msg_box_name.show()
            elif request_date < current_date or request_date > after_six_months:
                self.msg_box_name = QMessageBox()
                self.msg_box_name.setText("You can't book a date that is already passed or over 6 months!")
                self.msg_box_name.setWindowTitle("Notification")
                self.msg_box_name.show()
            elif request_date == current_date and request_time < after_two_hours:
                self.msg_box_name = QMessageBox()
                self.msg_box_name.setText("You can't book a time that is already passed or near!")
                self.msg_box_name.setWindowTitle("Notification")
                self.msg_box_name.show()
            else:
                request_date = request_date.toString(Qt.ISODate)
                request_time = request_time.toString("hh:mm:ss")
                conn = sqlite3.connect('call_a_doctor.db')
                cursor = conn.cursor()
                print('3')

                cursor.execute('SELECT * FROM Clinic WHERE Clinic_Name = ?', (clinic_name,))
                find_clinic_id = cursor.fetchone()
                clinic_id = find_clinic_id[0]

                cursor.execute('SELECT * FROM Doctor WHERE Doctor_Name = ?', (doctor_name,))
                find_doctor_id = cursor.fetchone()
                doctor_id = find_doctor_id[0]

                print(doctor_id)
                print(clinic_id)
                print(patient_id)

                cursor.execute('SELECT * FROM Patient_Request WHERE Doctor_ID = ?', (doctor_id,))
                find_date = cursor.fetchall()
                datetime_result = 0
                for items in find_date:
                    print(request_date)
                    print(request_time)
                    print(items[6])
                    print(items[7])
                    future_after_two_hours = datetime.strptime(items[7], "%H:%M:%S")
                    future_after_two_hours += timedelta(hours=2)
                    future_after_two_hours = future_after_two_hours.strftime("%H:%M:%S")
                    print("future two hours " + future_after_two_hours)
                    if request_date == items[6]:
                        if request_time < future_after_two_hours:
                            datetime_result = 1
                if datetime_result == 0:
                    insert_command = '''
                                     INSERT INTO Patient_Request (Patient_ID, Clinic_ID, Doctor_ID, 
                                     Request_State, Request_Date, Request_Reason, Request_Time)
                                     VALUES (?, ?, ?, ?, ?, ?, ?)
                                     '''
                    cursor.execute(insert_command, (patient_id, clinic_id, doctor_id, '0', request_date,
                                                    request_reason, request_time))
                    conn.commit()
                    self.msg_box_name = QMessageBox()
                    self.msg_box_name.setText("Request Sent Successfully.")
                    self.msg_box_name.setWindowTitle("Notification")
                    self.msg_box_name.show()
                    Request_Form.close()
                else:
                    self.msg_box_name = QMessageBox()
                    self.msg_box_name.setText("You cannot book a date that is near others request!")
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

        self.Request_dateEdit = QtWidgets.QDateTimeEdit(Request_Form)
        self.Request_dateEdit.setGeometry(QtCore.QRect(550, 90, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.Request_dateEdit.setFont(font)
        self.Request_dateEdit.setObjectName("Request_dateEdit")
        self.Request_dateEdit.setDateTime(QDateTime.currentDateTime())

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


