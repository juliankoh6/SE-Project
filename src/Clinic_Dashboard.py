import sys
import sqlite3
from PyQt5 import QtWidgets, uic

qtCreatorFile = "ClinicDashboard.ui"
Ui_ClinicDashboard, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Clinic_Dashboard(QtWidgets.QMainWindow, Ui_ClinicDashboard):
    def __init__(self, clinic_id):
        super(Clinic_Dashboard, self).__init__()
        self.setupUi(self)
        self.clinic_id = clinic_id
        self.displayClinicDetails()

        self.EditDetails.clicked.connect(self.edit_details)

    def displayClinicDetails(self):
        try:
            conn = sqlite3.connect("call_a_doctor.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Clinic_Name, Clinic_Speciality, Clinic_Email, Clinic_Location, Clinic_Contact_Number FROM Clinic WHERE Clinic_ID = ?",
                (self.clinic_id,))
            data = cursor.fetchone()

            if data:
                self.lineEditClinicName.setText(data[0])
                self.lineEditSpeciality.setText(data[1])
                self.lineEditEmail.setText(data[2])
                self.lineEditLocation.setText(data[3])
                self.lineEditContactNumber.setText(data[4])

            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def edit_details(self):
        self.edit_window = EditClinicDetails(self.clinic_id)
        self.edit_window.show()

class EditClinicDetails(QtWidgets.QMainWindow):
    def __init__(self, clinic_id):
        super(EditClinicDetails, self).__init__()
        uic.loadUi('Edit_Clinic_Details.ui', self)

        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.pushButton.clicked.connect(self.save_details)

        self.clinic_id = clinic_id
        self.load_clinic_details()

    def load_clinic_details(self):
        try:
            self.cursor.execute("SELECT * FROM Clinic WHERE Clinic_ID = ?", (self.clinic_id,))
            clinic = self.cursor.fetchone()

            if clinic:
                self.EditClinicName.setText(clinic[1])
                self.EditClinicEmail.setText(clinic[4])
                self.EditClinicLocation.setText(clinic[5])
                self.EditContactNumber.setText(clinic[6])

                specialties = clinic[7].split(', ') if clinic[7] else []
                for spec in specialties:
                    item = QtWidgets.QListWidgetItem(spec)
                    self.SpecialtyList.addItem(item)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_details(self):
        try:
            clinic_name = self.EditClinicName.text()
            specialties = sorted([self.SpecialtyList.item(i).text() for i in range(self.SpecialtyList.count())])
            clinic_specialty = ", ".join(specialties) if specialties else "Default"
            clinic_email = self.EditClinicEmail.text()
            clinic_location = self.EditClinicLocation.text()
            clinic_contact_number = self.EditContactNumber.text()

            self.cursor.execute("""
                UPDATE Clinic 
                SET Clinic_Name = ?, Clinic_Speciality = ?, Clinic_Email = ?, Clinic_Location = ?, Clinic_Contact_Number = ? 
                WHERE Clinic_ID = ?
            """, (clinic_name, clinic_specialty, clinic_email, clinic_location, clinic_contact_number, self.clinic_id))

            self.conn.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Clinic details updated successfully!")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 1  # This should be dynamically set based on the logged-in user
    window = Clinic_Dashboard(clinic_id)
    window.show()
    sys.exit(app.exec_())
