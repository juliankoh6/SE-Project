import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from CAD_Login import LoginApp

qtCreatorFile = "Clinic_Request.ui"  # Your UI file name
Ui_ClinicRequest, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicRequestApp(QtWidgets.QMainWindow, Ui_ClinicRequest):
    def __init__(self, clinic_id):
        super(ClinicRequestApp, self).__init__()
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.PatientsButton.clicked.connect(self.redirect_to_clinic_patient)
        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)
        self.DoctorsButton.clicked.connect(self.redirect_to_clinic_doctor)
        self.LogoutButton.clicked.connect(self.redirect_to_login)

        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

    def redirect_to_clinic_patient(self):
        from clinicpatients import ClinicPatientApp  # Local import to avoid circular dependency
        self.clinic_patient_window = ClinicPatientApp(self.clinic_id)
        self.clinic_patient_window.show()
        self.close()

    def redirect_to_clinic_dashboard(self):
        from Clinic_Dashboard import Clinic_Dashboard
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)
        self.clinicDashboardWindow.show()
        self.close()

    def redirect_to_clinic_doctor(self):
        from clinicdoctor import ClinicDoctorApp
        self.clinicDoctorWindow = ClinicDoctorApp(self.clinic_id)
        self.clinicDoctorWindow.show()
        self.close()

    def redirect_to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 8
    window = ClinicRequestApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
