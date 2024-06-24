import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtGui
from Clinic_Dashboard import Clinic_Dashboard
from PyQt5.QtWidgets import QMessageBox
from email_sender import encrypt
from CAD_Login import LoginApp


# Path to your .ui file
qtCreatorFile = "Clinic_Doctor.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicDoctorApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, clinic_id, parent=None):
        super(ClinicDoctorApp, self).__init__(parent)
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.IncomingRequestsButton.clicked.connect(self.redirect_to_clinic_incoming_request)
        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)
        self.MyRequestsButton.clicked.connect(self.redirect_to_clinic_requests)
        self.LogoutButton.clicked.connect(self.redirect_to_login)

        # Database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        # Setup UI
        self.initUI()
        self.load_doctors()
        self.populate_specialties()

    def initUI(self):
        self.RegisterDoctorButton.clicked.connect(self.register_doctor)
        self.SearchButton.clicked.connect(self.search_doctors)
        self.ShowAllButton.clicked.connect(self.load_doctors)
        self.Speciality.currentIndexChanged.connect(self.filter_doctors_by_specialty)
        self.DeleteDoctorButton.clicked.connect(self.delete_doctor)
        self.SpecialityListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.DoctorTable.itemSelectionChanged.connect(self.handle_doctor_selection)

    def populate_specialties(self):
        query = "SELECT DISTINCT Doctor_Speciality FROM Doctor WHERE Clinic_ID = ?"
        self.cursor.execute(query, (self.clinic_id,))
        specialties = self.cursor.fetchall()
        current_specialty = self.Speciality.currentText()
        self.Speciality.clear()
        self.Speciality.addItem("Show All", None)
        for specialty in specialties:
            self.Speciality.addItem(specialty[0], specialty[0])

        index = self.Speciality.findText(current_specialty)
        if index >= 0:
            self.Speciality.setCurrentIndex(index)
        else:
            self.Speciality.setCurrentIndex(0)

        self.populate_speciality_list_widget()

    def populate_speciality_list_widget(self):
        self.SpecialityListWidget.clear()
        query = "SELECT Clinic_Speciality FROM Clinic WHERE Clinic_ID = ?"
        self.cursor.execute(query, (self.clinic_id,))
        clinic_specialty = self.cursor.fetchone()
        if clinic_specialty:
            specialties = clinic_specialty[0].split(', ')
            for specialty in specialties:
                item = QtWidgets.QListWidgetItem(specialty)
                self.SpecialityListWidget.addItem(item)

    def filter_doctors_by_specialty(self):
        specialty = self.Speciality.currentText()
        if specialty == "Show All":
            self.load_doctors()
        else:
            self.load_doctors(specialty=specialty)

    def load_doctors(self, specialty=None, search_query=None):
        if search_query:
            query = "SELECT Doctor_Name, Doctor_Email, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ? AND Doctor_Name LIKE ?"
            self.cursor.execute(query, (self.clinic_id, f'%{search_query}%'))
        elif specialty and specialty != "Show All":
            query = "SELECT Doctor_Name, Doctor_Email, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ? AND Doctor_Speciality = ?"
            self.cursor.execute(query, (self.clinic_id, specialty))
        else:
            query = "SELECT Doctor_Name, Doctor_Email, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ?"
            self.cursor.execute(query, (self.clinic_id,))

        rows = self.cursor.fetchall()
        self.update_doctor_table(rows)

    def update_doctor_table(self, rows):
        self.DoctorTable.setRowCount(len(rows))
        self.DoctorTable.setColumnCount(3)
        self.DoctorTable.setHorizontalHeaderLabels(['Doctor Name', 'Doctor Email', 'Doctor Speciality'])

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.DoctorTable.setItem(row_index, column_index, item)

        header = self.DoctorTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def search_doctors(self):
        search_text = self.SearchDoctorInput.text().strip()
        if search_text:
            self.load_doctors(search_query=search_text)

    def handle_doctor_selection(self):
        selection = self.DoctorTable.selectionModel()
        if not selection.hasSelection():
            self.selected_doctor_name = None
        else:
            row_index = selection.currentIndex().row()
            self.selected_doctor_name = self.DoctorTable.item(row_index, 0).text()

    def delete_doctor(self):
        if not hasattr(self, 'selected_doctor_name') or not self.selected_doctor_name:
            QMessageBox.warning(self, "Selection Required", "Please select a doctor to delete.")
            return

        doctor_name = self.selected_doctor_name

        reply = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete the doctor '{doctor_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Doctor WHERE Doctor_Name = ? AND Clinic_ID = ?", (doctor_name, self.clinic_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Doctor deleted successfully.")
                self.load_doctors()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete doctor: {e}")

    def register_doctor(self):
        doctor_name = self.DoctorNameInput.text().strip()
        doctor_email = self.DoctorEmailInput.text().strip()
        doctor_job = self.DoctorJobInput.text().strip()
        doctor_specialties = [item.text() for item in self.SpecialityListWidget.selectedItems()]
        doctor_password = self.DoctorPasswordInput.text().strip()

        if not (doctor_name and doctor_email and doctor_job and doctor_password and doctor_specialties):
            QMessageBox.warning(self, "Application Error", "All fields must be filled and at least one specialty must be selected!")
            return

        self.cursor.execute("SELECT Doctor_ID FROM Doctor WHERE Doctor_Email = ?", (doctor_email,))
        if self.cursor.fetchone() is not None:
            QMessageBox.critical(self, "Registration Failed", "Email already exists.")
            return

        hashed_password = encrypt(doctor_password)

        try:
            self.cursor.execute("""
                INSERT INTO Doctor (Clinic_ID, Doctor_Name, Doctor_Email, Doctor_Job, Doctor_Password, Doctor_Speciality) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.clinic_id, doctor_name, doctor_email, doctor_job, hashed_password, ', '.join(doctor_specialties)))
            self.conn.commit()
            QMessageBox.information(self, "Registration Successful", "Doctor has been successfully registered!")
            self.populate_specialties()
            self.load_doctors()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def redirect_to_clinic_incoming_request(self):
        from clinicincomingrequest import ClinicIncomingRequestApp
        self.clinic_incoming_request_window = ClinicIncomingRequestApp(self.clinic_id)
        self.clinic_incoming_request_window.show()
        self.close()

    def redirect_to_clinic_requests(self):
        from clinicrequests import ClinicRequestsApp  # Local import to avoid circular dependency
        self.clinic_requests_window = ClinicRequestsApp(self.clinic_id)
        self.clinic_requests_window.show()
        self.close()

    def redirect_to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

    def redirect_to_clinic_dashboard(self):
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)
        self.clinicDashboardWindow.show()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 8  # This should be dynamically set based on the logged-in user
    window = ClinicDoctorApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
