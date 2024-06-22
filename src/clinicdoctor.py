import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from Clinic_Dashboard import Clinic_Dashboard
from PyQt5.QtWidgets import QMessageBox
from email_sender import encrypt

# Path to your .ui file
qtCreatorFile = "Clinic_Doctor.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicDoctorApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, clinic_id, parent=None):
        super(ClinicDoctorApp, self).__init__(parent)
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.RequestsButton.clicked.connect(self.redirect_to_clinic_request)
        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)

        # Database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        # Setup UI
        self.initUI()

    def initUI(self):
        self.RegisterDoctorButton.clicked.connect(self.register_doctor)

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message_dialog(self, title, message):
        QMessageBox.information(self, title, message)

    def register_doctor(self):
        doctor_name = self.DoctorNameInput.text().strip()
        doctor_email = self.DoctorEmailInput.text().strip()
        doctor_job = self.DoctorJobInput.text().strip()
        doctor_specialties = [item.text() for item in self.SpecialityListWidget.selectedItems()]
        doctor_password = self.DoctorPasswordInput.text().strip()
        doctor_status = self.DoctorStatus.currentText()

        # Convert status to integer
        status_map = {'Available': 1, 'Busy': 0}
        doctor_status_value = status_map.get(doctor_status, 1)

        # Validate inputs
        if not (doctor_name and doctor_email and doctor_job and doctor_password and doctor_specialties):
            QMessageBox.warning(self, "Application Error",
                                "All fields must be filled and at least one specialty must be selected!")
            return

        # Check if the email already exists
        self.cursor.execute("SELECT Doctor_ID FROM Doctor WHERE Doctor_Email = ?", (doctor_email,))
        if self.cursor.fetchone() is not None:
            QMessageBox.critical(self, "Registration Failed", "Email already exists.")
            return

        # Hash the password
        hashed_password = encrypt(doctor_password)

        # Insert the new doctor into the database
        self.cursor.execute("""
            INSERT INTO Doctor (Clinic_ID, Doctor_Name, Doctor_Email, Doctor_Job, Doctor_Password, Doctor_Speciality, Doctor_Status) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.clinic_id, doctor_name, doctor_email, doctor_job, hashed_password, ', '.join(doctor_specialties),
            doctor_status_value))
        self.conn.commit()
        QMessageBox.information(self, "Registration Successful", "Doctor has been successfully registered!")

    def redirect_to_clinic_request(self):
        from clinicrequest import ClinicRequestApp  # Local import to avoid circular dependency
        # Here, we instantiate and show the ClinicDoctorApp
        self.clinic_request_window = ClinicRequestApp(self.clinic_id)
        self.clinic_request_window.show()
        self.close()

    def redirect_to_clinic_dashboard(self):
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)  # Pass clinic_id
        self.clinicDashboardWindow.show()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 1
    window = ClinicDoctorApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
