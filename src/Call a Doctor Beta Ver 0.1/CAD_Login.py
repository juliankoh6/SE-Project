import sqlite3
from PyQt5.QtCore import Qt, QDateTime, QDate, QTime, QTimer
from email_sender import verify_password, send_email
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import sys
import re
import pytest

# Load the UI files
qtCreatorFile = "ui/CAD_login_page_ui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
qtAdminFile = 'ui/Admin_Dashboard_ui.ui'

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

        if email == "ADMIN" and password == "ADMIN":
            self.open_admin_dashboard()
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

        # Regular expression for validating an Email format
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            QMessageBox.warning(self, "Email Error", "Please enter a valid email address")
    
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
            if user_type == "Doctor":
                self.open_doctor_dashboard(user_id)
            elif user_type == "Patient":
                self.msg_box_name = QMessageBox()
                self.msg_box_name.setText(f"Welcome {user_type} {user_name}")
                self.msg_box_name.setWindowTitle("Login Successful")
                self.msg_box_name.setStandardButtons(QMessageBox.Ok)
                self.msg_box_name.show()
                self.open_patient_dashboard(user_id)
            elif user_type == "Clinic":
                QMessageBox.information(self, "Login Successful", f"Welcome {user_type} {user_name}")
                self.open_clinic_dashboard(user_id)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password")
            return

    # Open Admin Dashboard
    def open_admin_dashboard(self):
        self.close()
        self.admin_Dashboard_window = Admin_Dashboard()
        self.admin_Dashboard_window.show()

    # Open Doctor dashboard page for doctor user
    def open_doctor_dashboard(self, doctor_id):
        conn = sqlite3.connect('call_a_doctor.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Doctor WHERE Doctor_ID = ? AND Doctor_Status = 1", (doctor_id,))
        data = cursor.fetchone()
        if data:
            self.close()
            from doctor_dashboard import DoctorDashboard
            Clinic_id = data[1]
            user_name = data[2]
            print(Clinic_id)
            conn.close()
            QMessageBox.information(self, "Login Successful", f"Welcome Doctor {user_name}")
            self.doctor_dashboard_window = DoctorDashboard(doctor_id, Clinic_id)
            self.doctor_dashboard_window.show()
        else:
            self.msg_box_name = QMessageBox()
            self.msg_box_name.setText("This doctor has been deleted or not available!")
            self.msg_box_name.setWindowTitle("Notification")
            self.msg_box_name.show()

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

# Class that handles UI and functionality of the admin dashboard
class Admin_Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super(Admin_Dashboard, self).__init__()
        # Load the UI
        uic.loadUi(qtAdminFile, self)

        # Connect to the SQLite database
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.current_clinic = None
        self.load_pending_clinic()
        # Connect buttons to their respective functions
        self.Accept_Button.clicked.connect(self.accept_clinic)
        self.Reject_Button.clicked.connect(self.reject_clinic)
        self.Log_out.clicked.connect(self.redirect_to_login)

    # Load the first pending clinic from the database
    def load_pending_clinic(self):
        # Fetch the first clinic with status 0 (pending) from the database
        self.cursor.execute("SELECT * FROM Clinic WHERE Clinic_Status = 0")
        pending_clinic = self.cursor.fetchone()

        if pending_clinic:
            self.current_clinic = pending_clinic
            # Map the labels to the respective columns in the database
            labels = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
            columns = {
                'Clinic_Name': 'Clinic Name',
                'Clinic_Speciality': 'Clinic Specialty',
                'Owner_NRIC': 'Owner NRIC',
                'Clinic_Email': 'Clinic Email',
                'Clinic_Location': 'Clinic Location',
                'Clinic_Contact_Number': 'Clinic Contact Number'
            }
            column_indices = {
                'Clinic_Name': 1,
                'Clinic_Speciality': 2,
                'Owner_NRIC': 3,
                'Clinic_Email': 4,
                'Clinic_Location': 5,
                'Clinic_Contact_Number': 6
            }

            # Update the labels with the corresponding clinic information
            for label, col_name in zip(labels, columns.keys()):
                label.setText(f"{columns[col_name]}: {pending_clinic[column_indices[col_name]]}")
        else:
            # If no pending clinic is found, clear the labels
            self.current_clinic = None
            self.clear_labels()

    # Function to clear all labels if no remaining clinics that are pending approval
    def clear_labels(self):
        labels = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
        for label in labels:
            label.setText("")

    # Function to accept a clinic's application and send an email
    def accept_clinic(self):
        if self.current_clinic:
            clinic_id = self.current_clinic[0]
            clinic_email = self.current_clinic[4]

            # Update the clinic status to approved (1)
            self.cursor.execute("UPDATE Clinic SET Clinic_Status = 1 WHERE Clinic_ID = ?", (clinic_id,))
            self.conn.commit()

            # Send approval email
            subject = "Clinic Application Approved"
            body = "Congratulations! Your clinic application has been approved."
            send_email(clinic_email, subject, body)
            QtWidgets.QMessageBox.warning(self, "Clinic Accepted", "The clinic has been accepted and notified.")
            # Load the next pending clinic
            self.load_pending_clinic()
        else:
            QtWidgets.QMessageBox.warning(self, "No Pending Clinics", "There are no more clinics pending approval.")

    # Reject a clinic's application and send an email
    def reject_clinic(self):
        if self.current_clinic:
            clinic_id = self.current_clinic[0]
            clinic_email = self.current_clinic[4]
            reason = self.Reason.toPlainText().strip()

            # Send rejection email
            subject = "Clinic Application Rejected"
            body = "We regret to inform you that your clinic application has been rejected."
            if reason:
                body += f" Reason: {reason}"
            send_email(clinic_email, subject, body)

            # Delete the clinic from the database
            self.cursor.execute("DELETE FROM Clinic WHERE Clinic_ID = ?", (clinic_id,))
            self.conn.commit()
            QtWidgets.QMessageBox.warning(self, "Clinic Rejected", "The clinic has been successfully rejected.")
            # Load the next pending clinic
            self.load_pending_clinic()
        else:
            QtWidgets.QMessageBox.warning(self, "No Pending Clinics", "There are no more clinics pending approval.")

    # Log out to login page
    def redirect_to_login(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())

