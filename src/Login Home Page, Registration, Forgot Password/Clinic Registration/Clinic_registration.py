import sys
import sqlite3
import re
from email_sender import send_email
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# Main application class, Handles UI and functionality of the app
class ClinicRegisterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Clinic_registration_ui.ui', self)

        # Database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        # Initialize UI
        self.initUI()

    # Initialize the UI components and their signal
    def initUI(self):
        # Connect buttons to their respective functions
        self.VerifyEmail.clicked.connect(self.send_verification_email)
        self.SendApplication.clicked.connect(self.send_application)

        # Connect combo box changes to respective functions
        self.countrybox.currentIndexChanged.connect(self.on_country_changed)

        # Populate combo boxes with options
        self.populate_combo_boxes()

    # Populate country and state combo boxes with data from the database.
    def populate_combo_boxes(self):
        try:
            # Fetch countries from database
            self.cursor.execute("SELECT id, name FROM locations WHERE type = 'country'")
            countries = self.cursor.fetchall()

            # Add empty item to make nothing selected by default
            self.countrybox.addItem("")
            self.statebox.addItem("")

            # Add country items
            self.country_map = {}
            for country in countries:
                country_id, country_name = country
                self.countrybox.addItem(country_name)
                self.country_map[country_name] = country_id
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Could not fetch countries: {e}")

    # Update the states shown in state combo box based on the selected country.
    def on_country_changed(self):
        try:
            # Clear state combo box when country changes
            self.statebox.clear()

            # Add empty item to state combo box
            self.statebox.addItem("")

            # Only populating states box if country is selected
            selected_country = self.countrybox.currentText()
            if selected_country:
                country_id = self.country_map[selected_country]
                # Fetch states for the selected country from database
                self.cursor.execute("SELECT name FROM locations WHERE parent_id = ?", (country_id,))
                states = self.cursor.fetchall()
                for state in states:
                    self.statebox.addItem(state[0])
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Could not fetch states: {e}")

    # Display an error message dialog
    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    #Display an information message dialog.
    def show_message_dialog(self, title, message):
        QMessageBox.information(self, title, message)

    # Verify the email address entered by the user by asking user to check their inbox
    def send_verification_email(self, email):
        email = self.ClinicEmailInput.text()

        # Simple regex for validating an email
        regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if re.match(regex, email):
            try:
                subject = 'EMAIL VERIFICATION'
                body = ('Call A Doctor will be using this email as login credential if your clinic is approved, '
                        'continue with registration steps if you see this email')
                send_email(email, subject, body) 
                self.show_message_dialog("Email Verification",
                                         f"Email verification sent to {email}. Check your inbox (or spam folder) to ensure the correct email is entered.")
            except Exception as e:
                self.show_message_dialog("Email Verification", "An error occurred. Please try again later.")
                print(f"Error sending email: {e}")

    # Enters user input details into database table for pending applications after checking for errors
    def send_application(self):
        data = {
            'country': self.countrybox.currentText(),
            'state': self.statebox.currentText(),
            'clinic_name': self.ClinicNameInput.text(),
            'address_line1': self.addressLine1Input.text(),
            'address_line2': self.addressLine2Input.text(),
            'clinic_contact_number': self.ContactNumberInput.text(),
            'doctor_name': self.DoctorNameInput.text(),
            'graduated_from': self.InstitutionInput.text(),
            'type_of_registration': f"{self.TypeOfRegistration.currentText()} {self.TypeOfRegistrationInput.text()}",
            'clinic_email': self.ClinicEmailInput.text(),
            'password': self.PasswordInput.text(),
            'confirm_password': self.PasswordInput2.text()
        }

        # Error handling for inputs
        # Validate contact number
        if not data['clinic_contact_number'].isdigit() or len(data['clinic_contact_number']) < 10:
            QMessageBox.warning(self, "Application Error",
                                "Contact number must be at least 10 digits and contain only numbers.")
            return

        # Validate doctor name
        if not re.match(r'^[a-zA-Z\s]+$', data['doctor_name']):
            QMessageBox.warning(self, "Application Error",
                                "Doctor name must contain only alphabetic characters and spaces.")
            return

        # Make sure all fields are filled
        if not all(data.values()):
            QMessageBox.warning(self, "Application Error", "All fields must be filled!")
            return

        # Make sure password matches confirm password
        if f"{self.PasswordInput.text()}" != f"{self.PasswordInput2.text()}":
            QMessageBox.warning(self, "Application Error", "Password and confirm password do not match.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO clinics_pending_approval 
                (country, state, clinic_name, address_line1, address_line2, clinic_contact_number, doctor_name, graduated_from, type_of_registration, clinic_email, password) 
                VALUES (:country, :state, :clinic_name, :address_line1, :address_line2, :clinic_contact_number, :doctor_name, :graduated_from, :type_of_registration, :clinic_email, :password)
            """, data)
            self.conn.commit()
            QMessageBox.information(self, "Application Sent", "Your application has been sent!")
            self.clear_form()
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Could not send application: {e}")

    # Clears form after application is sent
    def clear_form(self):
        self.countrybox.setCurrentIndex(0)
        self.statebox.setCurrentIndex(0)
        self.ClinicNameInput.clear()
        self.addressLine1Input.clear()
        self.addressLine2Input.clear()
        self.ContactNumberInput.clear()
        self.DoctorNameInput.clear()
        self.InstitutionInput.clear()
        self.TypeOfRegistration.setCurrentIndex(0)
        self.TypeOfRegistrationInput.clear()
        self.EmailInput.clear()
        self.PasswordInput.clear()
        self.PasswordInput2.clear()


app = QtWidgets.QApplication(sys.argv)
window = ClinicRegisterApp()
window.show()
sys.exit(app.exec_())
