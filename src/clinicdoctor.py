import sys
from PyQt5 import QtWidgets, uic
from Clinic_Dashboard import Clinic_Dashboard

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
    clinic_id = 1
    window = ClinicDoctorApp(clinic_id)
    window.show()
    sys.exit(app.exec_())
