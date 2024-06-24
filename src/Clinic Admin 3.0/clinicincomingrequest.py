import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from CAD_Login import LoginApp


qtCreatorFile = "Clinic_Incoming_Requests.ui"  # Your UI file name
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
        self.RejectButton.clicked.connect(self.reject_request)
        self.AssignButton.clicked.connect(self.assign_request)

        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.load_incoming_requests()

    def load_incoming_requests(self):
        query = """
        SELECT p.Patient_Name, p.Patient_Gender, p.Patient_Birthdate, d.Doctor_Speciality, d.Doctor_Name, pr.Request_Date, pr.Request_Reason, pr.Request_ID
        FROM Patient_Request pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        JOIN Doctor d ON pr.Doctor_ID = d.Doctor_ID
        WHERE pr.Clinic_ID = ? AND pr.Request_State = 0
        """
        self.cursor.execute(query, (self.clinic_id,))
        rows = self.cursor.fetchall()

        self.IncomingRequestWidget.setRowCount(len(rows))
        self.IncomingRequestWidget.setColumnCount(8)
        self.IncomingRequestWidget.setHorizontalHeaderLabels(
            ['Patient Name', 'Gender', 'Birthday', 'Speciality', 'Doctor Name', 'Visit Date', 'Request Reason',
             'Request ID'])

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.IncomingRequestWidget.setItem(row_index, column_index, item)

        self.IncomingRequestWidget.setColumnHidden(7, True)  # Hide the Request ID column
        header = self.IncomingRequestWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)

    def reject_request(self):
        selection = self.IncomingRequestWidget.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "Selection Required", "Please select a request to reject.")
            return

        row_index = selection.currentIndex().row()
        request_id = self.IncomingRequestWidget.item(row_index, 7).text()

        try:
            self.cursor.execute("UPDATE Patient_Request SET Request_State = 2 WHERE Request_ID = ?", (request_id,))
            self.conn.commit()
            QMessageBox.information(self, "Request Rejected", "The request has been rejected.")
            self.load_incoming_requests()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to reject request: {e}")

    def assign_request(self):
        selection = self.IncomingRequestWidget.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "Selection Required", "Please select a request to assign.")
            return

        row_index = selection.currentIndex().row()
        request_id = self.IncomingRequestWidget.item(row_index, 7).text()

        try:
            self.cursor.execute("UPDATE Patient_Request SET Request_State = 1 WHERE Request_ID = ?", (request_id,))
            self.conn.commit()
            QMessageBox.information(self, "Request Assigned", "The request has been assigned.")
            self.load_incoming_requests()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to assign request: {e}")

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
