import sys
import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# Load the UI file
qtCreatorFile = "Call A doctor login page.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
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
        self.ForgotPasswordpushButton.clicked.connect(self.forgot_password)

    # Sign in user and error handling for invalid inputs
    def login(self):
        email = self.Email_line.text()
        password = self.Password_line.text()

        if not email and not password:
            QMessageBox.warning(self, "Input Error", "Please enter your email and password")
            return

        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        self.cursor.execute(query, (email, password))
        result = self.cursor.fetchone()

        if result:
            QMessageBox.information(self, "Login Successful", "Welcome!")

        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password")

    def register(self):
        QMessageBox.information(self, "Register", "Registration functionality not yet implemented")

    def forgot_password(self):
        QMessageBox.information(self, "Forgot Password", "Password recovery functionality not yet implemented")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CallADoctorApp()
    window.show()
    sys.exit(app.exec_())
