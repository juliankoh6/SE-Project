import sys
import sqlite3
from email_sender import send_email
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog

# Load the UI file
qtCreatorFile = "CAD_login_page_ui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Main application class, Handles UI and functionality of the app
class CallADoctorApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # Connect to SQLite database
        self.conn = sqlite3.connect("call_a_doctor.db")
        self.cursor = self.conn.cursor()

    def initUI(self):
        # Connect buttons to their respective functions
        self.LoginpushButton.clicked.connect(self.login)
        self.RegisterButton.clicked.connect(self.register)
        self.RegisterClinicButton.clicked.connect(self.register_clinic)
        self.ForgotPasswordpushButton.clicked.connect(self.forgot_password)

    # Sign in user and error handling for invalid inputs
    def login(self):
        email = self.Email_line.text()
        password = self.Password_line.text()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please enter your email and password")
            return

        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        self.cursor.execute(query, (email, password))
        result = self.cursor.fetchone()

        if result:
            QMessageBox.information(self, "Login Successful", "Welcome")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password")

    # Redirect to register page
    def register(self):
        from Register_page import RegisterAccountApp
        self.registration_window = RegisterAccountApp()
        self.registration_window.show()
        self.close()

    # Redirect to clinic registration page
    def register_clinic(self):
        from Clinic_registration import ClinicRegisterApp
        self.registration_clinic_window = ClinicRegisterApp()
        self.registration_clinic_window.show()
        self.close()

    # Retrieve forgotten password functionality
    def forgot_password(self):
        email, ok = QInputDialog.getText(self, 'Forgot Password', 'Enter your email:')

        if ok and email:
            query = "SELECT password FROM users WHERE email = ?"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()

            if result:
                password = result[0]
                subject = "Your Password"
                body = f"Your password for Call A Doctor is: {password}"
                try:
                    send_email(email, subject, body)
                    QMessageBox.information(self, "Email Sent", f"Password has been sent to {email}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not send email: {e}")
            else:
                QMessageBox.warning(self, "Error", "Email not found")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CallADoctorApp()
    window.show()
    sys.exit(app.exec_())
