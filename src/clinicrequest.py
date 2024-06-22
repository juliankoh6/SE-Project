import sys
from PyQt5 import QtWidgets, uic
from Clinic_Dashboard import Clinic_Dashboard
from CAD_Login import LoginApp


qtCreatorFile = "Clinic_Request.ui"  # Ensure the path to your .ui file is correct
Ui_ClinicRequest, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ClinicRequestApp(QtWidgets.QMainWindow, Ui_ClinicRequest):
    def __init__(self, clinic_id, parent=None):
        super(ClinicRequestApp, self).__init__(parent)
        self.setupUi(self)
        self.clinic_id = clinic_id

        self.DashboardButton.clicked.connect(self.redirect_to_clinic_dashboard)
        self.DoctorsButton.clicked.connect(self.redirect_to_clinic_doctor)
        self.LogoutButton.clicked.connect(self.redirect_to_login)

    def redirect_to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

    def redirect_to_clinic_doctor(self):
        from clinicdoctor import ClinicDoctorApp  # Local import to avoid circular dependency
        self.clinic_doctor_window = ClinicDoctorApp(self.clinic_id)
        self.clinic_doctor_window.show()
        self.close()

    def redirect_to_clinic_dashboard(self):
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)  # Pass clinic_id
        self.clinicDashboardWindow.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 1
    window = ClinicRequestApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
