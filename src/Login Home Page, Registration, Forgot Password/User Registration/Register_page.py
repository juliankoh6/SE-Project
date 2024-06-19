import sys
import sqlite3
import re
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from email_sender import encrypt

# Load the UI file
qtCreatorFile = "CAD_register_ui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


# Main application class, Handles UI and functionality of Register page
class RegisterAccountApp(QtWidgets.QMainWindow, Ui_MainWindow):
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

    def register_account(self):
        try:
            name = f"{self.NameInput.text().strip()} {self.LastNameInput.text().strip()}"
            email = self.emailInput.text()
            password = self.passwordInput.text()  # Note: Password should ideally be hashed before storage
            confirm_password = self.confirmPasswordInput.text()
            address = f"{self.addressLine1Input.text()}, {self.addressLine2Input.text()}"
            gender = self.GenderBox.currentText()
            birthdate = self.BirthdateEdit.date().toString("dd-MM-yyyy")
            number_type = self.NumberType.currentText()
            number_input = self.NumberInput.text()
            contact_number = self.contactNumberInput.text()

            # Check if all required fields are filled
            if not all(
                    [name.strip(), email, password, confirm_password, address.strip(), gender, birthdate, number_type,
                     number_input.strip(), contact_number.strip()]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields")
                return

            # Check if name only contains alphabets and allow spaces for unique names
            if not all(char.isalpha() or char.isspace() for char in name):
                QMessageBox.warning(self, "Name Error", "Name should only contain alphabets")
                return

            # Check if clinic contact number is not all digits or less than 10 digits
            if not contact_number.isdigit() or len(contact_number) < 10:
                QtWidgets.QMessageBox.warning(self, "Application Error", "Contact number must be at least 10 digits "
                                                    "and contain only numbers.")
                return

            # Regular expression for validating an Email
            if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
                QMessageBox.warning(self, "Email Error", "Please enter a valid email address")
                return

            # Check if email already exists
            self.cursor.execute("SELECT 1 FROM Patient WHERE Patient_Email = ?", (email,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Email Error", "Email already exists")
                return

            # Check if password and confirm password match
            if password != confirm_password:
                QMessageBox.warning(self, "Password Error", "Passwords do not match")
                return

            # Check if gender is selected
            if gender not in ["Male", "Female"]:
                QMessageBox.warning(self, "Gender Error", "Please select a gender")
                return

            # Combine selection of NRIC/Passport with the numbers
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

            # redirect to login
            self.redirect_to_login()

        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Could not register account: {e}")
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

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    # Return to login page
    def redirect_to_login(self):
        from CAD_Login import CallADoctorApp
        self.login_window = CallADoctorApp()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterAccountApp()
    window.show()
    sys.exit(app.exec_())
