import sys
import sqlite3
import re
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from email_sender import encrypt, send_email
from CAD_Login import LoginApp

# Load the UI files
qtCreatorFileRegister = "ui/CAD_register_ui.ui"
qtCreatorFileClinic = "ui/Clinic_registration_ui.ui"
Ui_RegisterWindow, QtBaseClassRegister = uic.loadUiType(qtCreatorFileRegister)
Ui_ClinicWindow, QtBaseClassClinic = uic.loadUiType(qtCreatorFileClinic)


# Main application class for RegisterAccount
class RegisterAccountApp(QtWidgets.QMainWindow, Ui_RegisterWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect to SQLite database
        try:
            self.conn = sqlite3.connect("call_a_doctor.db")
            self.cursor = self.conn.cursor()
            print("Database connection and cursor initialized successfully")
        except sqlite3.Error as e:
            self.show_error_message("Database Connection Error", f"Could not connect to database: {e}")

        self.initUI()

    def initUI(self):
        # Register user information
        self.RegisterButton.clicked.connect(self.register_account)
        # Return to Login Page
        self.commandLinkButton.clicked.connect(self.redirect_to_login)

    # Register patient account with input details after passing validation
    def register_account(self):
        try:
            name = f"{self.NameInput.text().strip()} {self.LastNameInput.text().strip()}"
            email = self.emailInput.text()
            password = self.passwordInput.text()
            confirm_password = self.confirmPasswordInput.text()
            address = f"{self.addressLine1Input.text()}, {self.addressLine2Input.text()}"
            gender = self.GenderBox.currentText()
            birthdate = self.BirthdateEdit.date().toString("dd-MM-yyyy")
            number_type = self.NumberType.currentText()
            number_input = self.NumberInput.text()
            contact_number = self.contactNumberInput.text()

            # Check if all required fields are filled
            if not all([name.strip(), email, password, confirm_password, address.strip(), gender, birthdate, number_type, number_input.strip(), contact_number.strip()]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields")
                return

            # Check if name only contains alphabets and allow spaces for unique names
            if not all(char.isalpha() or char.isspace() for char in name):
                QMessageBox.warning(self, "Name Error", "Name should only contain alphabets")
                return

            # Check if contact number is not all digits or less than 10 digits
            if not contact_number.isdigit() or len(contact_number) < 10:
                QtWidgets.QMessageBox.warning(self, "Application Error", "Contact number must be at least 10 digits and contain only numbers.")
                return

            # Regular expression for validating an Email
            if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
                QMessageBox.warning(self, "Email Error", "Please enter a valid email address")
                return

            # Check if email already exists in Patient table
            self.cursor.execute("SELECT 1 FROM Patient WHERE Patient_Email = ?", (email,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Email Error", "Email already exists")
                return

            # Check if password and confirm password match
            if password != confirm_password:
                QMessageBox.warning(self, "Password Error", "Passwords do not match")
                return

            # Only accept digits if NRIC type selected
            if number_type == "NRIC" and (not number_input.isdigit() or len(number_input) != 12):
                QtWidgets.QMessageBox.warning(self, "NRIC Error", "NRIC must be 12 digits and contain only numbers.")
                return

            # combining the number input with its type (NRIC/Passport)
            number = f"{number_type}: {number_input}"

            # Encode Password for security
            hashed_password = encrypt(password)

            # Insert new user into the Patient table
            query = """
                INSERT INTO Patient (Patient_Name, Patient_Email, Patient_Gender, Patient_Birthdate, Patient_IC_Passport, 
                Patient_Contact_Number, Patient_Address, Patient_Password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (name, email, gender, birthdate, number, contact_number, address, hashed_password))
            self.conn.commit()

            QMessageBox.information(self, "Registration Successful", "You have successfully registered!", QMessageBox.Ok, QMessageBox.Ok)
            self.clear_form()

            # redirect to login page
            self.redirect_to_login()

        except Exception as e:
            self.show_error_message("Error", f"An unexpected error occurred: {e}")

    # Clear form after input registration
    def clear_form(self):
        self.NameInput.clear()
        self.LastNameInput.clear()
        self.emailInput.clear()
        self.passwordInput.clear()
        self.confirmPasswordInput.clear()
        self.addressLine1Input.clear()
        self.addressLine2Input.clear()
        self.GenderBox.setCurrentIndex(0)
        self.BirthdateEdit.setDate(QtCore.QDate.currentDate())
        self.NumberType.setCurrentIndex(0)
        self.NumberInput.clear()
        self.contactNumberInput.clear()

    # Show Error messages for specific issues
    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    # Return to login page
    def redirect_to_login(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()

# Handles Clinic Registration page functionality and Ui buttons
class ClinicRegisterApp(QtWidgets.QMainWindow, Ui_ClinicWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Database connection
        try:
            self.conn = sqlite3.connect('call_a_doctor.db')
            self.cursor = self.conn.cursor()
            print("Database connection and cursor initialized successfully")
        except sqlite3.Error as e:
            self.show_error_message("Database Connection Error", f"Could not connect to database: {e}")

        self.initUI()

    def initUI(self):
        # Connect buttons to their respective functions
        self.VerifyEmail.clicked.connect(self.send_verification_email)
        self.SendApplication.clicked.connect(self.send_application)
        self.commandLinkButton.clicked.connect(self.redirect_to_login)

    # Show error message
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
                self.show_message_dialog("Email Verification", f"Email verification sent to {email}. Check your inbox to\
                ensure this is correct email.")
            except Exception as e:
                self.show_message_dialog("Email Verification", "An error occurred. Please try again later.")
                print(f"Error sending email: {e}")

    def send_application(self):
        # Collecting data from the form fields
        clinic_name = self.ClinicNameInput.text()
        address = f"{self.addressLine1Input.text()}, {self.addressLine2Input.text()}"
        clinic_contact_number = self.ContactNumberInput.text()
        clinic_email = self.ClinicEmailInput.text()
        owner_nric = self.Owner_NRIC.text()
        password = self.PasswordInput.text()
        confirm_password = self.PasswordInput2.text()
        specialties = sorted([item.text() for item in self.SpecialtyList.selectedItems()], key=str.lower)
        status = "0"
        
        # Error handling for inputs
        if not all([clinic_name, address, clinic_contact_number, clinic_email, owner_nric, password,
                    confirm_password]) or not specialties:
            QMessageBox.warning(self, "Application Error",
                                "All fields must be filled and at least one specialty must be selected!")
            return

        if len(specialties) > 6:
            QMessageBox.warning(self, "Application Error",
                                "You can only select a maximum of 6 specialties.")
            return

        # Check if contact number is not all digits or less than 10 digits
        if not clinic_contact_number.isdigit() or len(clinic_contact_number) < 10:
            QtWidgets.QMessageBox.warning(self, "Application Error",
                                          "Contact number must be at least 10 digits and contain only numbers.")
            return

        # Check if owner_nric is not all digits or not exactly 12 digits long
        if not owner_nric.isdigit() or len(owner_nric) != 12:
            QtWidgets.QMessageBox.warning(self, "NRIC Error", "NRIC must be 12 digits and contain only numbers.")
            return

        # Check if password entered matches the password confirmation
        if password != confirm_password:
            QMessageBox.warning(self, "Application Error", "Password and confirm password do not match.")
            return

        # Check if email already exists in Clinic table
        self.cursor.execute("SELECT 1 FROM Clinic WHERE Clinic_Email = ?", (clinic_email,))
        if self.cursor.fetchone():
            QMessageBox.warning(self, "Email Error", "Email already exists")
            return

        # Validate email format using regular expression
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', clinic_email):
            QMessageBox.warning(self, "Email Error", "Please enter a valid email address")
            return

        try:
            # Insert into database
            self.cursor.execute("""
                INSERT INTO Clinic
                (Clinic_Name, Clinic_Location, Clinic_Contact_Number, Clinic_Email, Owner_NRIC, Clinic_Password, 
                Clinic_Speciality, Clinic_Status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (clinic_name, address, clinic_contact_number, clinic_email, owner_nric, encrypt(password),
                  ', '.join(specialties), status))
            self.conn.commit()

            # Success message and form clearing
            self.show_message_dialog("Application Sent", "Your clinic application has been sent successfully.")
            self.clear_form()

            # Redirect to login page
            self.redirect_to_login()

        except Exception as e:
            self.show_error_message("Application Error", f"An error occurred: {e}")
            print(f"Application Error: {e}")

    # Clear form after successfully applied
    def clear_form(self):
        self.ClinicNameInput.clear()
        self.addressLine1Input.clear()
        self.addressLine2Input.clear()
        self.ContactNumberInput.clear()
        self.ClinicEmailInput.clear()
        self.Owner_NRIC.clear()
        self.PasswordInput.clear()
        self.PasswordInput2.clear()
        self.SpecialtyList.clearSelection()

    # Return to login page
    def redirect_to_login(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == 'ClinicRegistrationApp':
        window = ClinicRegisterApp()
    else:
        window = RegisterAccountApp()

    window.show()
    sys.exit(app.exec_())
