import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from CAD_Login import LoginApp

qtCreatorFile = "ui/ClinicDashboard.ui"
Ui_ClinicDashboard, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Clinic_Dashboard(QtWidgets.QMainWindow, Ui_ClinicDashboard):
    def __init__(self, clinic_id):
        super(Clinic_Dashboard, self).__init__()
        self.setupUi(self)
        self.clinic_id = clinic_id
        self.displayClinicDetails()

        self.EditDetails.clicked.connect(self.redirect_to_edit_details)
        self.LogoutButton.clicked.connect(self.redirect_to_login)
        self.DoctorsButton.clicked.connect(self.redirect_to_clinic_doctor)
        self.IncomingRequestsButton.clicked.connect(self.redirect_to_incoming_clinic_request)
        self.MyRequestsButton.clicked.connect(self.redirect_to_clinic_requests)

    def redirect_to_clinic_requests(self):
        from clinicrequests import ClinicRequestsApp  # Local import to avoid circular dependency
        self.clinic_requests_window = ClinicRequestsApp(self.clinic_id)
        self.clinic_requests_window.show()
        self.close()

    def redirect_to_incoming_clinic_request(self):
        from clinicincomingrequest import ClinicIncomingRequestApp  # Local import to avoid circular dependency
        self.clinic_incoming_request_window = ClinicIncomingRequestApp(self.clinic_id)
        self.clinic_incoming_request_window.show()
        self.close()

    def redirect_to_clinic_doctor(self):
        from clinicdoctor import ClinicDoctorApp  # Local import to avoid circular dependency
        self.clinic_doctor_window = ClinicDoctorApp(self.clinic_id)
        self.clinic_doctor_window.show()
        self.close()

    def redirect_to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

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
                self.lineEditSpeciality.setText(", ".join(sorted(set(data[1].split(", ")))))  # Ensure no duplicates
                self.lineEditEmail.setText(data[2])
                self.lineEditLocation.setText(data[3])
                self.lineEditContactNumber.setText(data[4])

            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def redirect_to_edit_details(self):
        from editdetails import EditClinicDetails
        self.clinic_edit_window = EditClinicDetails(self.clinic_id)
        self.clinic_edit_window.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
