import sys
import sqlite3
from email_sender import verify_password
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# Load the UI file
qtCreatorFile = "CAD_login_page_ui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


# Main application class. Handles UI and functionality of Login page
class CallADoctorApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # Initialize the main window and setup UI components
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # Connect to SQLite database
        try:
            self.conn = sqlite3.connect("call_a_doctor.db")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Unable to connect to the database: {str(e)}")
            sys.exit(1)

    def initUI(self):
        # Connect buttons to their respective functions
        self.LoginpushButton.clicked.connect(self.login)
        self.RegisterButton.clicked.connect(self.register_page)
        self.Clinics.clicked.connect(self.partnered_clinics_page)
        self.RegisterClinicButton.clicked.connect(self.register_clinic_page)
        self.ForgotPasswordpushButton.clicked.connect(self.forgot_password)

    def login(self):
        # Log in functionality
        try:
            email = self.Email_line.text()
            password = self.Password_line.text()
            user_type = self.UserType.currentText()

            if not email or not password:
                QMessageBox.warning(self, "Input Error", "Please enter your email and password")
                return

            if email == "ADMIN" and password == "ADMIN":
                self.open_admin_dashboard()
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

            query = f"SELECT {id_field}, {name_field}, {table}_Password FROM {table} WHERE {table}_Email = ?"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()

            if result:
                user_id, user_name, hashed_password = result

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
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email or password")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Database query failed: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")


    # Open Doctor dashboard page for doctor user
    def open_doctor_dashboard(self, doctor_id):
        # Open doctor's dashboard
        from Doctor_Dashboard import Doctor_Dashboard
        self.doctor_dashboard_window = Doctor_Dashboard(doctor_id)
        self.doctor_dashboard_window.show()
        self.close()

    # Open Doctor dashboard page for patient user
    def open_patient_dashboard(self, patient_id):
        # Open patient's dashboard
        from Patient_Dashboard import Patient_Dashboard
        self.patient_dashboard_window = Patient_Dashboard(patient_id)
        self.patient_dashboard_window.show()
        self.close()

    # Open Clinic Dashboard for Clinic admin
    def open_clinic_dashboard(self, clinic_id):
        # Open clinic's dashboard
        from Clinic_Dashboard import Clinic_Dashboard
        self.clinic_dashboard_window = Clinic_Dashboard(clinic_id)
        self.clinic_dashboard_window.show()
        self.close()

    # Open Admin dashboard for Application Admin
    def open_admin_dashboard(self):
        # Open admin dashboard
        from Admin_Dashboard import Admin_Dashboard
        self.admin_dashboard_window = Admin_Dashboard()
        self.admin_dashboard_window.show()
        self.close()


    # Open patient registration page
    def register_page(self):
        # Open user registration page
        from Register_page import RegisterAccountApp
        self.registration_window = RegisterAccountApp()
        self.registration_window.show()
        self.close()

    # Open clinic registration page
    def register_clinic_page(self):
        # Open clinic registration page
        from Clinic_registration import ClinicRegisterApp
        self.registration_clinic_window = ClinicRegisterApp()
        self.registration_clinic_window.show()
        self.close()

    # Open Partnered clinics page
    def partnered_clinics_page(self):
        # Open partnered clinics information page
        from Clinics_Info import ClinicInfo
        self.partnered_clinics_window = ClinicInfo()
        self.partnered_clinics_window.show()
        self.close()

    # Open Forgot Password page
    def forgot_password(self):
        # Open password retrieval page
        from ForgotPassword import ForgotPassword
        self.forgot_password_window = ForgotPassword()
        self.forgot_password_window.show()
        self.close()


# Handles UI and functionality of Partnered Clinics page
class ClinicInfo(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClinicInfo, self).__init__()
        uic.loadUi('Partnered_clinics_ui.ui', self)

        # Set up the database connection
        self.db = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.db.cursor()

        # Retrieve clinic data that are approved
        self.cursor.execute(
            "SELECT Clinic_ID, Clinic_Name, Clinic_Speciality, Clinic_Contact_Number, Clinic_Location FROM Clinic "
            "WHERE Clinic_Status = 1")
        clinics = self.cursor.fetchall()

        self.scroll_area = self.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setObjectName("scrollWidget")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # Populate the layout with clinic data
        for clinic in clinics:
            self.fill_clinic(clinic)

        self.commandLinkButton.clicked.connect(self.redirect_to_login)
        self.show()

    # Add Frames of clinics with their info to the page
    def fill_clinics(self, clinic):
        clinic_id, clinic_name, speciality, contact_number, address = clinic

        # Create a frame for each clinic
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # Create a vertical layout for the frame
        vbox = QtWidgets.QVBoxLayout()

        # Add clinic details to each frame
        vbox.addWidget(QtWidgets.QLabel(f"{clinic_name}"))
        vbox.addWidget(QtWidgets.QLabel(f"Specialties: {speciality}"))
        vbox.addWidget(QtWidgets.QLabel(f"Contact Number: {contact_number}"))
        vbox.addWidget(QtWidgets.QLabel(f"Address: {address}"))

        # Add a button to view doctors
        btn_view_doctors = QtWidgets.QPushButton("View Doctors")
        btn_view_doctors.clicked.connect(lambda: self.view_doctors(clinic_id))
        vbox.addWidget(btn_view_doctors)

        # Set the layout to the frame
        frame.setLayout(vbox)

        # Add the frame to the scroll area layout
        self.scroll_layout.addWidget(frame)

    # View information of doctors of respective clinics
    def view_doctors(self, clinic_id):
        self.cursor.execute("SELECT Doctor_Name, Doctor_Job, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ?"
                            , (clinic_id,))
        doctors = self.cursor.fetchall()

        # Display doctors in a message box
        if doctors:
            doctor_info = "\n\n".join(
                f"Name: {doctor[0]}\nJob: {doctor[1]}\nSpecialty: {doctor[2]}" for doctor in doctors)
            QtWidgets.QMessageBox.information(self, "Doctors Information", f"Doctors for this clinic:\n\n{doctor_info}")
        else:
            QtWidgets.QMessageBox.information(self, "No Doctors", "No doctors found for this clinic.")

    # Return to Login page
    def redirect_to_login(self):
        self.login_window = CallADoctorApp()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CallADoctorApp()
    window.show()
    sys.exit(app.exec_())
