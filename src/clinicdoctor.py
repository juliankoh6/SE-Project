import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtGui
from Clinic_Dashboard import Clinic_Dashboard
from PyQt5.QtWidgets import QMessageBox
from email_sender import encrypt

# Path to your .ui file
qtCreatorFile = "Clinic_Doctor.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicDoctorApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, clinic_id, parent=None):
        super(ClinicDoctorApp, self).__init__(parent)
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.RequestsButton.clicked.connect(self.redirect_to_clinic_request)
        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)

        # Database connection
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        # Setup UI
        self.initUI()
        self.load_doctors()
        self.populate_specialties()

    def initUI(self):
        self.RegisterDoctorButton.clicked.connect(self.register_doctor)
        self.SearchButton.clicked.connect(self.search_doctors)  # Ensure this is correctly connected
        self.ShowAllButton.clicked.connect(lambda: self.load_doctors())  # Resets the doctor list
        self.Speciality.currentIndexChanged.connect(
            self.filter_doctors_by_specialty)  # Ensure this is called only when the index actually changes
        self.DeleteDoctorButton.clicked.connect(self.delete_doctor)  # Connect the delete function
        self.ToggleStatusButton.clicked.connect(self.toggle_status)  # Connect the toggle status function

    def populate_specialties(self):
        query = "SELECT DISTINCT Doctor_Speciality FROM Doctor WHERE Clinic_ID = ?"
        self.cursor.execute(query, (self.clinic_id,))
        specialties = self.cursor.fetchall()
        current_specialty = self.Speciality.currentText()
        self.Speciality.clear()
        self.Speciality.addItem("Show All", None)
        for specialty in specialties:
            self.Speciality.addItem(specialty[0], specialty[0])

        # Set back the previously selected specialty if it still exists
        index = self.Speciality.findText(current_specialty)
        if index >= 0:
            self.Speciality.setCurrentIndex(index)
        else:
            self.Speciality.setCurrentIndex(0)  # Default to 'Show All' if not found

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

    def showEvent(self, event):
        super().showEvent(event)
        self.populate_specialties()  # Ensure the latest list of specialties is always displayed when the view becomes visible

    def filter_doctors_by_specialty(self):
        specialty = self.Speciality.currentData()
        if specialty:
            self.load_doctors(specialty)

    def load_doctors(self, specialty=None, search_query=None):
        if search_query:
            query = "SELECT Doctor_Name, Doctor_Status, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ? AND Doctor_Name LIKE ?"
            self.cursor.execute(query, (self.clinic_id, f'%{search_query}%'))
        elif specialty and specialty != "Show All":
            query = "SELECT Doctor_Name, Doctor_Status, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ? AND Doctor_Speciality = ?"
            self.cursor.execute(query, (self.clinic_id, specialty))
        else:
            query = "SELECT Doctor_Name, Doctor_Status, Doctor_Speciality FROM Doctor WHERE Clinic_ID = ?"
            self.cursor.execute(query, (self.clinic_id,))

        rows = self.cursor.fetchall()
        self.update_doctor_table(rows)

    def update_doctor_table(self, rows):
        self.DoctorTable.setRowCount(len(rows))
        self.DoctorTable.setColumnCount(3)  # For Name, Status, and Specialty
        self.DoctorTable.setHorizontalHeaderLabels(['Doctor Name', 'Doctor Status', 'Doctor Specialty'])

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                if column_index == 1:  # Convert status to text and color
                    if data == 1:
                        item.setText('Available')
                        item.setForeground(QtGui.QColor('green'))
                    else:
                        item.setText('Busy')
                        item.setForeground(QtGui.QColor('red'))
                self.DoctorTable.setItem(row_index, column_index, item)

        header = self.DoctorTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def search_doctors(self):
        search_text = self.SearchDoctorInput.text().strip()
        if search_text:  # Ensure there's text to search for
            self.load_doctors(search_query=search_text)

    def delete_doctor(self):
        selection = self.DoctorTable.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "Selection Required", "Please select a doctor to delete.")
            return

        # Assuming the first column contains the Doctor_Name
        row_index = selection.currentIndex().row()
        doctor_name = self.DoctorTable.item(row_index, 0).text()  # Adjust the index if necessary

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete the doctor '{doctor_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Doctor WHERE Doctor_Name = ? AND Clinic_ID = ?", (doctor_name, self.clinic_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Doctor deleted successfully.")
                self.load_doctors()  # Refresh the list
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete doctor: {e}")

    def toggle_status(self):
        selection = self.DoctorTable.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "Selection Required", "Please select a doctor to toggle status.")
            return

        # Assuming the first column contains the Doctor_Name
        row_index = selection.currentIndex().row()
        doctor_name = self.DoctorTable.item(row_index, 0).text()
        current_status = self.DoctorTable.item(row_index, 1).text()
        new_status = 0 if current_status == 'Available' else 1  # Toggle status

        try:
            self.cursor.execute("UPDATE Doctor SET Doctor_Status = ? WHERE Doctor_Name = ? AND Clinic_ID = ?",
                                (new_status, doctor_name, self.clinic_id))
            self.conn.commit()
            self.load_doctors()  # Refresh the list
            QMessageBox.information(self, "Success", "Doctor status updated successfully.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update doctor status: {e}")

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_message_dialog(self, title, message):
        QMessageBox.information(self, title, message)

    def register_doctor(self):
        doctor_name = self.DoctorNameInput.text().strip()
        doctor_email = self.DoctorEmailInput.text().strip()
        doctor_job = self.DoctorJobInput.text().strip()
        doctor_specialties = [item.text() for item in self.SpecialityListWidget.selectedItems()]
        doctor_password = self.DoctorPasswordInput.text().strip()
        doctor_status = self.DoctorStatus.currentText()

        # Convert status to integer
        status_map = {'Available': 1, 'Busy': 0}
        doctor_status_value = status_map.get(doctor_status, 1)

        # Validate inputs
        if not (doctor_name and doctor_email and doctor_job and doctor_password and doctor_specialties):
            QMessageBox.warning(self, "Application Error",
                                "All fields must be filled and at least one specialty must be selected!")
            return

        # Check if the email already exists
        self.cursor.execute("SELECT Doctor_ID FROM Doctor WHERE Doctor_Email = ?", (doctor_email,))
        if self.cursor.fetchone() is not None:
            QMessageBox.critical(self, "Registration Failed", "Email already exists.")
            return

        # Hash the password
        hashed_password = encrypt(doctor_password)

        # Insert the new doctor into the database
        try:
            self.cursor.execute("""
                INSERT INTO Doctor (Clinic_ID, Doctor_Name, Doctor_Email, Doctor_Job, Doctor_Password, Doctor_Speciality, Doctor_Status) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.clinic_id, doctor_name, doctor_email, doctor_job, hashed_password, ', '.join(doctor_specialties),
                  doctor_status_value))
            self.conn.commit()
            QMessageBox.information(self, "Registration Successful", "Doctor has been successfully registered!")
            self.populate_specialties()  # Refresh the specialties in the combobox
            self.load_doctors()  # Refresh the doctor table
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def redirect_to_clinic_request(self):
        from clinicrequest import ClinicRequestApp  # Local import to avoid circular dependency
        # Here, we instantiate and show the ClinicDoctorApp
        self.clinic_request_window = ClinicRequestApp(self.clinic_id)
        self.clinic_request_window.show()
        self.close()

    def redirect_to_clinic_dashboard(self):
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)  # Pass clinic_id
        self.clinicDashboardWindow.show()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 8
    window = ClinicDoctorApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
