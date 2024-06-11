import sqlite3
import re
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from CAD_Login import CallADoctorApp

# Load the UI file
qtCreatorFile = "CAD_register.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class RegisterAccountApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect to SQLite database
        try:
            self.conn = sqlite3.connect("call_a_doctor.db")  # Ensure this path is correct
            self.cursor = self.conn.cursor()
            print("Database connection and cursor initialized successfully")
        except sqlite3.Error as e:
            self.show_error_message("Database Connection Error", f"Could not connect to database: {e}")

        self.initUI()

    def initUI(self):
        # Connect buttons to their respective functions
        self.RegisterButton.clicked.connect(self.register_account)

        # Assuming commandLinkButton is a part of the UI setup
        self.commandLinkButton.clicked.connect(self.redirect_to_login)

        # Connect combo box changes to respective functions
        self.countrybox.currentIndexChanged.connect(self.on_country_changed)

        # Populate combo boxes with options
        self.populate_combo_boxes()

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

    def register_account(self):
        try:
            name = self.NameInput.text()
            username = self.Username.text()
            email = self.emailInput.text()
            password = self.passwordInput.text()
            confirm_password = self.confirmPasswordInput.text()
            address_line1 = self.addressLine1Input.text()
            address_line2 = self.addressLine2Input.text()
            state = self.statebox.currentText()
            country = self.countrybox.currentText()
            role = 'Patient'  # Default role


            # Check if name only contains alphabets
            if not re.match(r"^[A-Za-z]+$", name):
                QMessageBox.warning(self, "Name Error", "Name should only contain alphabets")
                return

            # Check if username already exists
            self.cursor.execute("SELECT 1 FROM Users WHERE Username = ?", (username,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Username Error", "Username already exists")
                return

            # Check if email format is valid
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                QMessageBox.warning(self, "Email Error", "Please enter a valid email address")
                return

            # Check if email already exists
            self.cursor.execute("SELECT 1 FROM Users WHERE Email = ?", (email,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Email Error", "Email already exists")
                return

            # Check if password and confirm password match
            if password != confirm_password:
                QMessageBox.warning(self, "Password Error", "Passwords do not match")
                return

            # Check if all required fields are filled
            if not all([name, username, email, password, confirm_password, address_line1, state, country]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields")
                return

            # Insert new user into the Users table
            query = """
                INSERT INTO Users (name, Username, Email, Password, address_line1, address_line2, state, country, Role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (name, username, email, password, address_line1, address_line2, state, country, role))
            self.conn.commit()

            QMessageBox.information(self, "Registration Successful", "You have successfully registered!", QMessageBox.Ok, QMessageBox.Ok)
            # Clear the form after successful registration
            self.clear_form()

            # After showing the confirmation message, redirect to login
            self.redirect_to_login()
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Could not register account: {e}")
        except Exception as e:
            self.show_error_message("Error", f"An unexpected error occurred: {e}")

    # Clear form after input registered
    def clear_form(self):
        self.NameInput.clear()
        self.Username.clear()
        self.emailInput.clear()
        self.passwordInput.clear()
        self.confirmPasswordInput.clear()
        self.addressLine1Input.clear()
        self.addressLine2Input.clear()
        self.statebox.setCurrentIndex(0)
        self.countrybox.setCurrentIndex(0)

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    def redirect_to_login(self):
        self.login_window = CallADoctorApp()
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterAccountApp()
    window.show()
    sys.exit(app.exec_())
