import sqlite3
from email_sender import verify_password
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import re

# Load the UI file
qtCreatorFile = "ui/CAD_login_page_ui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


# Main application class. Handles UI and functionality of Login page
class LoginApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # Initialize the main window and setup UI components
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # Connect to SQLite database
        self.conn = sqlite3.connect("call_a_doctor.db")
        self.cursor = self.conn.cursor()

    def initUI(self):
        # Connect buttons to their respective functions
        self.LoginpushButton.clicked.connect(self.login)
        self.RegisterButton.clicked.connect(self.register_page)
        self.Clinics.clicked.connect(self.partnered_clinics_page)
        self.RegisterClinicButton.clicked.connect(self.register_clinic_page)
        self.ForgotPasswordpushButton.clicked.connect(self.forgot_password)

    # Log in user after checking entered credentials
    def login(self):
        # Log in functionality
        email = self.Email_line.text().strip()
        password = self.Password_line.text().strip()
        user_type = self.UserType.currentText()

        # Regular expression for validating an Email format
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            QMessageBox.warning(self, "Email Error", "Please enter a valid email address")
            return

        # Check if both email and password filled properly
        if not email and not password:
            QMessageBox.warning(self, "Input Error", "Please enter your email and password")
            return
        elif not email:
            QMessageBox.warning(self, "Input Error", "Please enter your email")
            return
        elif not password:
            QMessageBox.warning(self, "Input Error", "Please enter your password")
            return

        # Determine the table and fields to query based on the user type
        table = ""
        id_field = ""
        name_field = ""
        if user_type == "Patient":
            table = "Patient"
            id_field = "Patient_ID"
            name_field = "Patient_Name"
        elif user_type == "Doctor":
            table = "Doctor"
            id_field = "Doctor_ID"
            name_field = "Doctor_Name"
        elif user_type == "Clinic":
            table = "Clinic"
            id_field = "Clinic_ID"
            name_field = "Clinic_Name"

        query = f"SELECT {id_field}, {name_field}, {table}_Password"
        if user_type == "Clinic":
            query += f", Clinic_Status FROM Clinic WHERE Clinic_Email = ?"
        else:
            query += f" FROM {table} WHERE {table}_Email = ?"

        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()

        # Check if the result is None
        if not result:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password")
            return

        user_id = result[0]
        user_name = result[1]
        hashed_password = result[2]

        if user_type == "Clinic":
            clinic_status = result[3]
            if clinic_status != 1:
                QMessageBox.warning(self, "Login Failed", "Your Clinic has not been approved yet")
                return

        # Verify if password entered matches hashed password
        if verify_password(password, hashed_password):
            QMessageBox.information(self, "Login Successful", f"Welcome {user_type} {user_name}")
            if user_type == "Doctor":
                self.open_doctor_dashboard(user_id)
            elif user_type == "Patient":
                self.open_patient_dashboard(user_id)
            elif user_type == "Clinic":
                self.open_clinic_dashboard(user_id)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password")

    # Open Doctor dashboard page for doctor user
    def open_doctor_dashboard(self, doctor_id):
        self.close()
        from Doctor_Dashboard import Doctor_Dashboard
        self.doctor_dashboard_window = Doctor_Dashboard(doctor_id)
        self.doctor_dashboard_window.show()

    # Open Doctor dashboard page for patient user
    def open_patient_dashboard(self, patient_id):
        self.close()
        from Patient_Dashboard import Patient_Dashboard
        self.patient_dashboard_window = Patient_Dashboard(patient_id)
        self.patient_dashboard_window.show()

    # Open Clinic Dashboard for Clinic admin
    def open_clinic_dashboard(self, clinic_id):
        self.close()
        from Clinic_Dashboard import Clinic_Dashboard
        self.clinic_dashboard_window = Clinic_Dashboard(clinic_id)
        self.clinic_dashboard_window.show()

    # Open Admin dashboard for Application Admin
    def open_admin_dashboard(self):
        self.close()
        from Admin_Dashboard import Admin_Dashboard
        self.admin_dashboard_window = Admin_Dashboard()
        self.admin_dashboard_window.show()

    # Open Patient Register page
    def register_page(self):
        self.close()
        from Registration import RegisterAccountApp
        self.registration_window = RegisterAccountApp()
        self.registration_window.show()

    # Open Clinic Registration page (will be pending approval before officially registered)
    def register_clinic_page(self):
        self.close()
        from Registration import ClinicRegisterApp
        self.registration_clinic_window = ClinicRegisterApp()
        self.registration_clinic_window.show()

    # Open Partnered clinics page
    def partnered_clinics_page(self):
        self.close()
        from Clinics_Info import ClinicInfo
        self.partnered_clinics_window = ClinicInfo()
        self.partnered_clinics_window.show()

    # Open Forgot password page
    def forgot_password(self):
        self.close()
        from ForgotPassword import ForgotPassword
        self.forgot_password_window = ForgotPassword()
        self.forgot_password_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
