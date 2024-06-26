import sys
import random
import string
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import sqlite3
from email_sender import send_email, encrypt
from CAD_Login import LoginApp


# Handles UI and functionality of Forgot Password page
class ForgotPassword(QtWidgets.QMainWindow):
    def __init__(self):
        super(ForgotPassword, self).__init__()
        uic.loadUi('ui/ForgotPassword_ui.ui', self)

        # Connect the buttons to the methods
        self.SendToken.clicked.connect(self.send_token)
        self.EnterToken.clicked.connect(self.enter_token)
        self.ReturnToLogin.clicked.connect(self.redirect_to_login)

        # Initialize database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

    # Send token to email of respective user type
    def send_token(self):
        email = self.Email_line.text()
        user_type = self.UserType.currentText()

        # Check if the email field is empty
        table = ""
        if user_type == "Patient":
            table = "Patient"
        elif user_type == "Doctor":
            table = "Doctor"
        elif user_type == "Clinic":
            table = "Clinic"

        if user_type == "Clinic":
            query = f"SELECT Clinic_Email, Clinic_Status FROM Clinic WHERE Clinic_Email = ?"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()

            if result:
                clinic_status = result[1]
                if clinic_status != 1:
                    QMessageBox.warning(self, "Error", "Your Clinic has not been approved yet")
                    return
                else:
                    token = self.generate_token()
                    update_query = f"UPDATE Clinic SET Clinic_Token = ? WHERE Clinic_Email = ?"
                    self.cursor.execute(update_query, (token, email))
                    self.conn.commit()
                    subject = "Password Reset Token"
                    body = f"Your password reset token for Call A Doctor is: {token}"
                    send_email(email, subject, body)
                    QMessageBox.information(self, "Email Sent", f"Token has been sent to {email}")
            else:
                QMessageBox.warning(self, "Error", "Clinic Email not found")
        else:
            query = f"SELECT {table}_Email FROM {table} WHERE {table}_Email = ?"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()

            if result:
                token = self.generate_token()
                update_query = f"UPDATE {table} SET {table}_Token = ? WHERE {table}_Email = ?"
                self.cursor.execute(update_query, (token, email))
                self.conn.commit()
                subject = "Password Reset Token"
                body = f"Your password reset token for Call A Doctor is: {token}"
                send_email(email, subject, body)
                QMessageBox.information(self, "Email Sent", f"Token has been sent to {email}")
            else:
                QMessageBox.warning(self, "Error", "Email not found")

    # Generate token consisting of random string of letters and digits
    def generate_token(self, length=20):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    # Check if the token entered is valid by checking database
    def enter_token(self):
        email = self.Email_line.text()
        token = self.Token_line.text()
        user_type = self.UserType.currentText()

        # Determine the table to query based on user type
        table = ""
        if user_type == "Patient":
            table = "Patient"
        elif user_type == "Doctor":
            table = "Doctor"
        elif user_type == "Clinic":
            table = "Clinic"

        query = f"SELECT {table}_Token FROM {table} WHERE {table}_Email = ?"
        try:
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()

            if result and result[0] == token:
                self.open_reset_password(email, table)
            else:
                QMessageBox.warning(self, "Error", "Invalid token.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Database error: {e}")

    # Open reset password page
    def open_reset_password(self, email, table):
        self.reset_password_window = ResetPassword(email, table)
        self.reset_password_window.show()
        self.close()

    # Return to login page
    def redirect_to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()


# Class that handles functionality and UI of Reset Password page
class ResetPassword(QtWidgets.QMainWindow):
    def __init__(self, email, table):
        super(ResetPassword, self).__init__()
        uic.loadUi('ui/ResetPassword_ui.ui', self)

        self.email = email
        self.table = table

        # Connect the button to the method
        self.SET.clicked.connect(self.reset_password)

        # Initialize database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

    # Function for letting user set their new password
    def reset_password(self):
        new_password = self.NewPassword.text()
        confirm_password = self.ConfirmPassword.text()

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        try:
            hashed_password = encrypt(new_password)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Encryption error: {e}")
            return

        query = f"UPDATE {self.table} SET {self.table}_Password = ?, {self.table}_Token = NULL WHERE {self.table}_Email = ?"
        try:
            self.cursor.execute(query, (hashed_password, self.email))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Password has been reset.")
            self.redirect_to_login()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Database error: {e}")

    # Return to login page
    def redirect_to_login(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ForgotPassword()
    window.show()
    sys.exit(app.exec_())
