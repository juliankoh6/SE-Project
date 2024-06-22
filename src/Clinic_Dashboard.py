import sys
import sqlite3
from PyQt5 import QtWidgets, uic

qtCreatorFile = "Clinic_Dashboard.ui"  # Path to your .ui file
Ui_ClinicDashboard, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicDashboard(QtWidgets.QMainWindow, Ui_ClinicDashboard):
    def __init__(self, clinic_id):
        super(ClinicDashboard, self).__init__()
        self.setupUi(self)  # Initialize the UI
        self.clinic_id = clinic_id
        self.displayClinicDetails()

    def displayClinicDetails(self):
        """Fetches clinic details from the database and displays them."""
        try:
            conn = sqlite3.connect("call_a_doctor.db")  # Ensure this is the correct path to your database
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Clinic_Name, Clinic_Speciality, Clinic_Email, Clinic_Location, Clinic_Contact_Number FROM Clinic WHERE Clinic_ID = ?",
                (self.clinic_id,))
            data = cursor.fetchone()

            if data:
                # Assuming your QLineEdit widget names are set correctly in your .ui file
                self.ClinicName.setText(data[0])  # Update these names based on actual object names in Qt Designer
                self.Speciality.setText(data[1])
                self.Email.setText(data[2])
                self.Location.setText(data[3])
                self.ContactNumber.setText(data[4])

            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ClinicDashboard(1)  # Assuming 1 is a valid clinic ID for testing
    window.show()
    sys.exit(app.exec_())
