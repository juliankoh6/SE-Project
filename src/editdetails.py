import sys
import sqlite3
from PyQt5 import QtWidgets, uic

# Class for Clinic Details Modification page
class EditClinicDetails(QtWidgets.QMainWindow):
    def __init__(self):
        super(EditClinicDetails, self).__init__()
        # Load the UI
        uic.loadUi('Edit_Clinic_Details.ui', self)

        # Connect to the SQLite database
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        # Connect the Save Details button to the save_details function
        self.pushButton.clicked.connect(self.save_details)

        self.load_clinic_details()

    def load_clinic_details(self):
        # Fetch clinic details from the database
        clinic_id = 5  # test
        self.cursor.execute("SELECT * FROM Clinic WHERE Clinic_ID = ?", (clinic_id,))
        clinic = self.cursor.fetchone()

        if clinic:
            # Map the UI elements to the database columns
            self.EditClinicName.setText(clinic[1])
            self.EditClinicEmail.setText(clinic[4])
            self.EditClinicLocation.setText(clinic[5])
            self.EditContactNumber.setText(clinic[6])

    def save_details(self):
        clinic_name = self.EditClinicName.text()
        specialties = sorted([self.SpecialtyList.item(i).text() for i in range(self.SpecialtyList.count())])
        clinic_specialty = ", ".join(specialties)
        clinic_email = self.EditClinicEmail.text()
        clinic_location = self.EditClinicLocation.text()
        clinic_contact_number = self.EditClinicContactNumber.text()

        # Update the database with the new details
        clinic_id = 5  # test
        self.cursor.execute("""
            UPDATE Clinic 
            SET Clinic_Name = ?, Clinic_Specialty = ?, Clinic_Email = ?, Clinic_Location = ?, Clinic_Contact_Number = ? 
            WHERE Clinic_ID = ?
        """, (clinic_name, clinic_specialty, clinic_email, clinic_location, clinic_contact_number, clinic_id))

        self.conn.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Clinic details updated successfully!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditClinicDetails()
    window.show()
    sys.exit(app.exec_())
