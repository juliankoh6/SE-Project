import sys
import sqlite3
from PyQt5 import QtCore, QtWidgets, uic
from CAD_Login import LoginApp

qtCreatorFile = "Clinic_Requests.ui"  # Your UI file name
Ui_ClinicRequests, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CustomDateEdit(QtWidgets.QDateEdit):
    def __init__(self, parent=None):
        super(CustomDateEdit, self).__init__(parent)
        self.setDisplayFormat("dd/MM/yyyy")
        self.setCalendarPopup(True)
        self.clear()  # Clear the initial date

    def clear(self):
        self.setSpecialValueText("Select Date")
        self.setDate(QtCore.QDate(2000, 1, 1))
        self.lineEdit().setText("")

    def date(self):
        if self.lineEdit().text() == "Select Date" or self.lineEdit().text() == "":
            return None
        return super(CustomDateEdit, self).date()

    def focusInEvent(self, event):
        if self.lineEdit().text() == "":
            self.setDate(QtCore.QDate.currentDate())
        super(CustomDateEdit, self).focusInEvent(event)

class ClinicRequestsApp(QtWidgets.QMainWindow, Ui_ClinicRequests):
    def __init__(self, clinic_id):
        super(ClinicRequestsApp, self).__init__()
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.ChooseDate = CustomDateEdit(self)
        self.ChooseDate.setGeometry(QtCore.QRect(350, 140, 151, 41))

        self.IncomingRequestsButton.clicked.connect(self.redirect_to_incoming_clinic_request)
        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)
        self.DoctorsButton.clicked.connect(self.redirect_to_clinic_doctor)
        self.LogoutButton.clicked.connect(self.redirect_to_login)
        self.ApplyButton.clicked.connect(self.apply_filters)
        self.ClearAllButton.clicked.connect(self.clear_all_filters)
        self.PatientTable.cellClicked.connect(self.load_patient_details)

        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.load_patient_requests()
        self.setup_table_headers()

    def setup_table_headers(self):
        self.PatientTable.setHorizontalHeaderLabels(
            ['Request ID', 'Patient Name', 'Requested Date', 'Requested Time', 'Request Status']
        )
        self.PatientDetailsTable.setHorizontalHeaderLabels(
            ['Email Address', 'Contact Number', 'Gender', 'Birthday', 'IC / Passport', 'Address']
        )
        self.RequestInfoTable.setHorizontalHeaderLabels(
            ['Request ID', 'Doctor', 'Speciality', 'Request Reason']
        )

        self.stretch_table_headers(self.PatientTable)
        self.stretch_table_headers(self.PatientDetailsTable)
        self.stretch_table_headers(self.RequestInfoTable)

    def stretch_table_headers(self, table_widget):
        header = table_widget.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(header.count() - 1, QtWidgets.QHeaderView.Stretch)

    def load_patient_requests(self):
        query = """
        SELECT pr.Request_ID, p.Patient_Name, pr.Request_Date, pr.Request_Time, 
               CASE pr.Request_State 
                   WHEN 1 THEN 'Accepted' 
                   WHEN 2 THEN 'Rejected' 
               END as Request_Status
        FROM Patient_Request pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        WHERE pr.Clinic_ID = ? AND pr.Request_State IN (1, 2)
        """
        self.cursor.execute(query, (self.clinic_id,))
        rows = self.cursor.fetchall()

        self.PatientTable.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.PatientTable.setItem(row_index, column_index, item)

        self.stretch_table_headers(self.PatientTable)

    def apply_filters(self):
        status_filter = self.PatientRequestStatus.currentText()
        selected_date = self.ChooseDate.date().toString("yyyy-MM-dd") if self.ChooseDate.date() else ''
        search_name = self.SearchPatientInput.text().strip()

        query = """
        SELECT pr.Request_ID, p.Patient_Name, pr.Request_Date, pr.Request_Time, 
               CASE pr.Request_State 
                   WHEN 1 THEN 'Accepted' 
                   WHEN 2 THEN 'Rejected' 
               END as Request_Status
        FROM Patient_Request pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        WHERE pr.Clinic_ID = ? 
        AND (? = '' OR p.Patient_Name LIKE ?) 
        AND (? = '' OR pr.Request_Date = ?)
        """
        params = [self.clinic_id, search_name, f'%{search_name}%', selected_date, selected_date]

        if status_filter == 'Accepted':
            query += " AND pr.Request_State = 1"
        elif status_filter == 'Rejected':
            query += " AND pr.Request_State = 2"
        elif status_filter == 'Show All':
            query += " AND pr.Request_State IN (1, 2)"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        self.PatientTable.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.PatientTable.setItem(row_index, column_index, item)

        self.stretch_table_headers(self.PatientTable)

    def clear_all_filters(self):
        self.SearchPatientInput.clear()
        self.PatientRequestStatus.setCurrentIndex(0)
        self.ChooseDate.clear()
        self.load_patient_requests()

        # Clear the PatientDetailsTable and RequestInfoTable
        self.PatientDetailsTable.setRowCount(0)
        self.RequestInfoTable.setRowCount(0)

    def load_patient_details(self, row, column):
        request_id = self.PatientTable.item(row, 0).text()

        query = """
        SELECT p.Patient_Email, p.Patient_Contact_Number, p.Patient_Gender, p.Patient_Birthdate, p.Patient_IC_Passport, p.Patient_Address
        FROM Patient_Request pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        WHERE pr.Request_ID = ?
        """
        self.cursor.execute(query, (request_id,))
        details = self.cursor.fetchone()

        self.PatientDetailsTable.setRowCount(1)
        for col_index, data in enumerate(details):
            item = QtWidgets.QTableWidgetItem(str(data))
            self.PatientDetailsTable.setItem(0, col_index, item)

        # Resize columns to fit content and then stretch the last column
        self.PatientDetailsTable.resizeColumnsToContents()
        header = self.PatientDetailsTable.horizontalHeader()
        header.setSectionResizeMode(header.count() - 1, QtWidgets.QHeaderView.Stretch)

        query = """
        SELECT pr.Request_ID, d.Doctor_Name, d.Doctor_Speciality, pr.Request_Reason
        FROM Patient_Request pr
        JOIN Doctor d ON pr.Doctor_ID = d.Doctor_ID
        WHERE pr.Request_ID = ?
        """
        self.cursor.execute(query, (request_id,))
        request_info = self.cursor.fetchone()

        self.RequestInfoTable.setRowCount(1)
        for col_index, data in enumerate(request_info):
            item = QtWidgets.QTableWidgetItem(str(data))
            self.RequestInfoTable.setItem(0, col_index, item)

        # Resize columns to fit content and then stretch the last column
        self.RequestInfoTable.resizeColumnsToContents()
        header = self.RequestInfoTable.horizontalHeader()
        header.setSectionResizeMode(header.count() - 1, QtWidgets.QHeaderView.Stretch)

    def redirect_to_incoming_clinic_request(self):
        from clinicincomingrequest import ClinicIncomingRequestApp  # Local import to avoid circular dependency
        self.clinic_request_window = ClinicIncomingRequestApp(self.clinic_id)
        self.clinic_request_window.show()
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

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 8
    window = ClinicRequestsApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
