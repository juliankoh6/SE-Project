import sys
import sqlite3
import re
from email_sender import send_email
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from email_sender import encrypt


# Handles UI and functionality of Register Clinic page
class ClinicRegisterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Clinic_registration_ui.ui", self)

        # Database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        # Initialize UI
        self.initUI()

    def initUI(self):
        # Connect buttons to their respective functions
        self.VerifyEmail.clicked.connect(self.send_verification_email)
        self.SendApplication.clicked.connect(self.send_application)
        self.commandLinkButton.clicked.connect(self.redirect_to_login)

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message_dialog(self, title, message):
        QMessageBox.information(self, title, message)

    # Sends email to inbox of inputted email to confirm email
    def send_verification_email(self):
        email = self.ClinicEmailInput.text()

        # Regular expression for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.match(regex, email):
            try:
                subject = 'EMAIL VERIFICATION'
                body = ('Call A Doctor will be using this email as login credential if your clinic is approved, '
                        'continue with registration steps if you see this email')
                send_email(email, subject, body)
                self.show_message_dialog("Email Verification",
                                         f"Email verification sent to {email}. Check your inbox to ensure this is correct email.")
            except Exception as e:
                self.show_message_dialog("Email Verification", "An error occurred. Please try again later.")
                print(f"Error sending email: {e}")

    def send_application(self):
        # Collecting data from the form
        data = {
            'clinic_name': self.ClinicNameInput.text(),
            'address': f"{self.addressLine1Input.text()}, {self.addressLine2Input.text()}",
            'clinic_contact_number': self.ContactNumberInput.text(),
            'clinic_email': self.ClinicEmailInput.text(),
            'owner_nric': self.Owner_NRIC.text(),
            'password': self.PasswordInput.text(),
            'confirm_password': self.PasswordInput2.text(),
            'specialties': sorted([item.text() for item in self.SpecialtyList.selectedItems()], key=str.lower),
            'status': "0"
        }

        # Error handling for inputs
        if not all(data.values()) or not data['specialties']:
            QMessageBox.warning(self, "Application Error",
                                "All fields must be filled and at least one specialty must be selected!")
            return

        # Check if clinic_contact_number is not all digits or less than 10 digits
        if not data['clinic_contact_number'].isdigit() or len(data['clinic_contact_number']) < 10:
            QtWidgets.QMessageBox.warning(self, "Application Error",
                                          "Contact number must be at least 10 digits and contain only numbers.")
            return

        # Check if password entered matches the password confirmation
        if data['password'] != data['confirm_password']:
            QMessageBox.warning(self, "Application Error", "Password and confirm password do not match.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO Clinic
                (Clinic_Name, Clinic_Location, Clinic_Contact_Number, Clinic_Email, Owner_NRIC, Clinic_Password, Clinic_Speciality, Clinic_Status) 
                VALUES (:clinic_name, :address, :clinic_contact_number, :clinic_email, :owner_nric, :password, :specialties, :status)
            """, {
                'clinic_name': data['clinic_name'],
                'address': data['address'],
                'clinic_contact_number': data['clinic_contact_number'],
                'clinic_email': data['clinic_email'],
                'owner_nric': data['owner_nric'],
                'password': encrypt(data['password']),
                'specialties': ", ".join(data['specialties']),
                'status': "0"
            })
            self.conn.commit()
            QMessageBox.information(self, "Application Sent", "Your application has been sent!")
            self.clear_form()
            # redirect to login page
            self.redirect_to_login()

        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Could not send application: {e}")

    # Clear input fields
    def clear_form(self):
        self.ClinicNameInput.clear()
        self.addressLine1Input.clear()
        self.addressLine2Input.clear()
        self.ContactNumberInput.clear()
        self.Owner_NRIC.clear()
        self.ClinicEmailInput.clear()
        self.PasswordInput.clear()
        self.PasswordInput2.clear()
        self.SpecialtyList.clearSelection()

    # Return to login page
    def redirect_to_login(self):
        from CAD_Login import CallADoctorApp
        self.login_window = CallADoctorApp()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ClinicRegisterApp()
    window.show()
    sys.exit(app.exec_())
