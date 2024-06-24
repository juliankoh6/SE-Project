import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from email_sender import send_email  # Import the email sending function
from CAD_Login import LoginApp

qtCreatorFile = "ui/Clinic_Incoming_Requests.ui"  # Your UI file name
Ui_ClinicRequest, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicIncomingRequestApp(QtWidgets.QMainWindow, Ui_ClinicRequest):
    def __init__(self, clinic_id):
        super(ClinicIncomingRequestApp, self).__init__()
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.MyRequestsButton.clicked.connect(self.redirect_to_clinic_patient)
        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)
        self.DoctorsButton.clicked.connect(self.redirect_to_clinic_doctor)
        self.LogoutButton.clicked.connect(self.redirect_to_login)
        self.RejectButton.clicked.connect(self.confirm_reject_request)
        self.AssignButton.clicked.connect(self.confirm_assign_request)

        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.load_incoming_requests()
        self.load_clinic_name()

    def load_incoming_requests(self):
        query = """
        SELECT pr.Request_ID, p.Patient_Name, p.Patient_Gender, p.Patient_Birthdate, 
               d.Doctor_Name, pr.Request_Date, pr.Request_Time, pr.Request_Reason, p.Patient_Email
        FROM Patient_Request pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        JOIN Doctor d ON pr.Doctor_ID = d.Doctor_ID
        WHERE pr.Clinic_ID = ? AND pr.Request_State = 0
        """
        self.cursor.execute(query, (self.clinic_id,))
        rows = self.cursor.fetchall()

        self.IncomingRequestWidget.setRowCount(len(rows))
        self.IncomingRequestWidget.setColumnCount(9)
        self.IncomingRequestWidget.setHorizontalHeaderLabels(
            ['Request ID', 'Patient Name', 'Gender', 'Birthday', 'Doctor Name', 'Visit Date', 'Visit Time', 'Request Reason', 'Patient Email'])

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.IncomingRequestWidget.setItem(row_index, column_index, item)

        header = self.IncomingRequestWidget.horizontalHeader()
        for col in range(header.count()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(header.count() - 1, QtWidgets.QHeaderView.Stretch)

    def load_clinic_name(self):
        query = "SELECT Clinic_Name FROM Clinic WHERE Clinic_ID = ?"
        self.cursor.execute(query, (self.clinic_id,))
        result = self.cursor.fetchone()
        if result:
            self.clinic_name = result[0]
        else:
            self.clinic_name = "Your Clinic"

    def confirm_reject_request(self):
        selection = self.IncomingRequestWidget.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "Selection Required", "Please select a request to reject.")
            return

        row_index = selection.currentIndex().row()
        request_id = self.IncomingRequestWidget.item(row_index, 0).text()

        reply = QMessageBox.question(self, 'Confirm Reject', f'Are you sure you want to reject Request ID {request_id}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reject_request(request_id)

    def confirm_assign_request(self):
        selection = self.IncomingRequestWidget.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "Selection Required", "Please select a request to assign.")
            return

        row_index = selection.currentIndex().row()
        request_id = self.IncomingRequestWidget.item(row_index, 0).text()

        reply = QMessageBox.question(self, 'Confirm Assign', f'Are you sure you want to assign Request ID {request_id}?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.assign_request(request_id)

    def reject_request(self, request_id):
        try:
            # Get patient and request details
            query = """
            SELECT p.Patient_Email, pr.Request_ID, pr.Request_Reason, d.Doctor_Name, pr.Request_Date, pr.Request_Time
            FROM Patient_Request pr
            JOIN Patient p ON pr.Patient_ID = p.Patient_ID
            JOIN Doctor d ON pr.Doctor_ID = d.Doctor_ID
            WHERE pr.Request_ID = ?
            """
            self.cursor.execute(query, (request_id,))
            patient_email, request_id, request_reason, doctor_name, request_date, request_time = self.cursor.fetchone()

            self.cursor.execute("UPDATE Patient_Request SET Request_State = 2 WHERE Request_ID = ?", (request_id,))
            self.conn.commit()
            QMessageBox.information(self, "Request Rejected", f"Request ID {request_id} has been rejected.")
            self.load_incoming_requests()

            # Send email notification
            subject = "Your Request has been Rejected"
            body = (f"Dear Patient,\n\n"
                    f"Your request with the following details has been rejected by the clinic:\n\n"
                    f"Request ID: {request_id}\n"
                    f"Request Reason: {request_reason}\n"
                    f"Doctor: {doctor_name}\n"
                    f"Visit Date: {request_date}\n"
                    f"Visit Time: {request_time}\n\n"
                    f"We apologize for any inconvenience caused.\n\n"
                    f"Best regards,\n{self.clinic_name}")
            send_email(patient_email, subject, body)
            QMessageBox.information(self, "Email Sent", "A notification email has been sent to the patient.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to reject request: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Email Error", f"Failed to send rejection email: {e}")

    def assign_request(self, request_id):
        try:
            # Get patient and request details
            query = """
            SELECT p.Patient_Email, pr.Request_ID, pr.Request_Reason, d.Doctor_Name, pr.Request_Date, pr.Request_Time
            FROM Patient_Request pr
            JOIN Patient p ON pr.Patient_ID = p.Patient_ID
            JOIN Doctor d ON pr.Doctor_ID = d.Doctor_ID
            WHERE pr.Request_ID = ?
            """
            self.cursor.execute(query, (request_id,))
            patient_email, request_id, request_reason, doctor_name, request_date, request_time = self.cursor.fetchone()

            self.cursor.execute("UPDATE Patient_Request SET Request_State = 1 WHERE Request_ID = ?", (request_id,))
            self.conn.commit()
            QMessageBox.information(self, "Request Assigned", f"Request ID {request_id} has been assigned.")
            self.load_incoming_requests()

            # Send email notification
            subject = "Your Request has been Accepted"
            body = (f"Dear Patient,\n\n"
                    f"Your request with the following details has been accepted by the clinic:\n\n"
                    f"Request ID: {request_id}\n"
                    f"Request Reason: {request_reason}\n"
                    f"Doctor: {doctor_name}\n"
                    f"Visit Date: {request_date}\n"
                    f"Visit Time: {request_time}\n\n"
                    f"Best regards,\n{self.clinic_name}")
            send_email(patient_email, subject, body)
            QMessageBox.information(self, "Email Sent", "A notification email has been sent to the patient.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to assign request: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Email Error", f"Failed to send assignment email: {e}")

    def redirect_to_clinic_patient(self):
        from clinicrequests import ClinicRequestsApp  # Local import to avoid circular dependency
        self.clinic_patient_window = ClinicRequestsApp(self.clinic_id)
        self.clinic_patient_window.show()
        self.close()

    def redirect_to_clinic_dashboard(self):
        from Clinic_Dashboard import Clinic_Dashboard
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)
        self.clinicDashboardWindow.show()
        self.close()

    def redirect_to_clinic_doctor(self):
        from clinicdoctor import ClinicDoctorApp
        self.clinicDoctorWindow = ClinicDoctorApp(self.clinic_id)
        self.clinicDoctorWindow.show()
        self.close()

    def redirect_to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 8
    window = ClinicIncomingRequestApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
