import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from email_sender import encrypt, send_email
from CAD_Login import LoginApp

# Path to your .ui file
qtCreatorFile = "Clinic_Doctor.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicDoctorApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, clinic_id, parent=None):
        super(ClinicDoctorApp, self).__init__(parent)
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.IncomingRequestsButton.clicked.connect(self.redirect_to_clinic_incoming_request)
        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)
        self.MyRequestsButton.clicked.connect(self.redirect_to_clinic_requests)
        self.LogoutButton.clicked.connect(self.redirect_to_login)
        self.VerifyButton.clicked.connect(self.verify_email)

        # Database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        # Setup UI
        self.initUI()
        self.populate_specialties()

        # Load all doctors initially
        self.load_doctors()

        # Track verified emails
        self.verified_emails = {}

    def initUI(self):
        self.RegisterDoctorButton.clicked.connect(self.register_doctor)
        self.ApplyButton.clicked.connect(self.search_doctors)
        self.ShowAllButton.clicked.connect(self.show_all_doctors)
        self.DeleteDoctorButton.clicked.connect(self.delete_doctor)
        self.ClearFormButton.clicked.connect(self.clear_form)
        self.SpecialityListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.DoctorTable.itemSelectionChanged.connect(self.handle_doctor_selection)

    def populate_specialties(self):
        query = "SELECT DISTINCT Doctor_Speciality FROM Doctor WHERE Clinic_ID = ? AND Doctor_Status = 1"
        self.cursor.execute(query, (self.clinic_id,))
        specialties = self.cursor.fetchall()
        current_specialty = self.Speciality.currentText()
        self.Speciality.clear()
        self.Speciality.addItem("Show All", None)
        for specialty in specialties:
            self.Speciality.addItem(specialty[0], specialty[0])

        index = self.Speciality.findText(current_specialty)
        if index >= 0:
            self.Speciality.setCurrentIndex(index)
        else:
            self.Speciality.setCurrentIndex(0)

        self.populate_speciality_list_widget()

    def populate_speciality_list_widget(self):
        self.SpecialityListWidget.clear()
        query = "SELECT Clinic_Speciality FROM Clinic WHERE Clinic_ID = ?"
        self.cursor.execute(query, (self.clinic_id,))
        clinic_specialty = self.cursor.fetchone()
        if clinic_specialty:
            specialties = clinic_specialty[0].split(', ')
            for specialty in specialties:
                item = QtWidgets.QListWidgetItem(specialty)
                self.SpecialityListWidget.addItem(item)

    def search_doctors(self):
        search_text = self.SearchDoctorInput.text().strip()
        specialty = self.Speciality.currentText()

        if specialty == "Show All":
            specialty = None

        self.load_doctors(specialty=specialty, search_query=search_text)

    def load_doctors(self, specialty=None, search_query=None):
        query = "SELECT Doctor_Name, Doctor_Email, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ? AND Doctor_Status = 1"
        params = [self.clinic_id]

        if specialty and specialty != "Show All":
            query += " AND Doctor_Speciality = ?"
            params.append(specialty)

        if search_query:
            query += " AND Doctor_Name LIKE ?"
            params.append(f'%{search_query}%')

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        self.update_doctor_table(rows)

    def update_doctor_table(self, rows):
        self.DoctorTable.setRowCount(len(rows))
        self.DoctorTable.setColumnCount(3)
        self.DoctorTable.setHorizontalHeaderLabels(['Doctor Name', 'Doctor Email', 'Doctor Speciality'])

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.DoctorTable.setItem(row_index, column_index, item)

        header = self.DoctorTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def handle_doctor_selection(self):
        selection = self.DoctorTable.selectionModel()
        if not selection.hasSelection():
            self.selected_doctor_name = None
        else:
            row_index = selection.currentIndex().row()
            self.selected_doctor_name = self.DoctorTable.item(row_index, 0).text()
            self.load_doctor_info(self.selected_doctor_name)

    def load_doctor_info(self, doctor_name):
        query = """
        SELECT pr.Request_ID, pr.Request_Date, pr.Request_Time, p.Patient_Name
        FROM Patient_Request pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        JOIN Doctor d ON pr.Doctor_ID = d.Doctor_ID
        WHERE d.Doctor_Name = ? AND pr.Request_State = 1
        """
        self.cursor.execute(query, (doctor_name,))
        rows = self.cursor.fetchall()

        self.DoctorInfoTable.setRowCount(len(rows))
        self.DoctorInfoTable.setColumnCount(4)
        self.DoctorInfoTable.setHorizontalHeaderLabels(['Request ID', 'Visit Date', 'Visit Time', 'Patient Name'])

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.DoctorInfoTable.setItem(row_index, column_index, item)

        header = self.DoctorInfoTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def clear_form(self):
        self.DoctorTable.clearSelection()
        self.DoctorInfoTable.setRowCount(0)

    def show_all_doctors(self):
        self.Speciality.setCurrentIndex(self.Speciality.findText("Show All"))
        self.SearchDoctorInput.clear()
        self.load_doctors()

    def delete_doctor(self):
        if not hasattr(self, 'selected_doctor_name') or not self.selected_doctor_name:
            QMessageBox.warning(self, "Selection Required", "Please select a doctor to delete.")
            return

        doctor_name = self.selected_doctor_name

        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete the doctor '{doctor_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("UPDATE Doctor SET Doctor_Status = 0 WHERE Doctor_Name = ? AND Clinic_ID = ?",
                                    (doctor_name, self.clinic_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", f"Doctor {doctor_name} is resigned.")
                self.load_doctors()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Failed to update doctor status: {e}")

    def register_doctor(self):
        doctor_name = self.DoctorNameInput.text().strip()
        doctor_email = self.DoctorEmailInput.text().strip()
        doctor_job = self.DoctorJobInput.text().strip()
        doctor_specialties = [item.text() for item in self.SpecialityListWidget.selectedItems()]
        doctor_password = self.DoctorPasswordInput.text().strip()

        if not (doctor_name and doctor_email and doctor_job and doctor_password and doctor_specialties):
            QMessageBox.warning(self, "Application Error",
                                "All fields must be filled and at least one specialty must be selected!")
            return

        if doctor_email not in self.verified_emails or not self.verified_emails[doctor_email]:
            QMessageBox.critical(self, "Registration Failed", "Email not verified.")
            return

        self.cursor.execute("SELECT Doctor_ID FROM Doctor WHERE Doctor_Email = ?", (doctor_email,))
        if self.cursor.fetchone() is not None:
            QMessageBox.critical(self, "Registration Failed", "Email already exists.")
            return

        hashed_password = encrypt(doctor_password)

        try:
            self.cursor.execute("""
                INSERT INTO Doctor (Clinic_ID, Doctor_Name, Doctor_Email, Doctor_Job, Doctor_Password, Doctor_Speciality, Doctor_Status) 
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (
            self.clinic_id, doctor_name, doctor_email, doctor_job, hashed_password, ', '.join(doctor_specialties)))
            self.conn.commit()
            QMessageBox.information(self, "Registration Successful", "Doctor has been successfully registered!")
            self.populate_specialties()
            self.load_doctors()

            # Send registration success email
            subject = "Registration Successful"
            body = f"Dear {doctor_name},\n\nYour account has been successfully registered.\n\nEmail: {doctor_email}\nPassword: {doctor_password}\n\nPlease use these credentials to login to the app."
            send_email(doctor_email, subject, body)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def verify_email(self):
        sender_email = "kohjulian150@gmail.com"
        sender_password = "lbon slns xpev edgb"
        receiver_email = self.DoctorEmailInput.text().strip()
        subject = "Email Verification"
        body = "Your current email is verified."

        try:
            send_email(receiver_email, subject, body, sender_email, sender_password)
            QMessageBox.information(self, "Email Verification", "Verification email sent successfully.")
            self.verified_emails[receiver_email] = True
        except Exception as e:
            QMessageBox.critical(self, "Email Error", f"Failed to send verification email: {e}")

    def redirect_to_clinic_incoming_request(self):
        from clinicincomingrequest import ClinicIncomingRequestApp
        self.clinic_incoming_request_window = ClinicIncomingRequestApp(self.clinic_id)
        self.clinic_incoming_request_window.show()
        self.close()

    def redirect_to_clinic_requests(self):
        from clinicrequests import ClinicRequestsApp  # Local import to avoid circular dependency
        self.clinic_requests_window = ClinicRequestsApp(self.clinic_id)
        self.clinic_requests_window.show()
        self.close()

    def redirect_to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

    def redirect_to_clinic_dashboard(self):
        from Clinic_Dashboard import Clinic_Dashboard
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)
        self.clinicDashboardWindow.show()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 8  # This should be dynamically set based on the logged-in user
    window = ClinicDoctorApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
