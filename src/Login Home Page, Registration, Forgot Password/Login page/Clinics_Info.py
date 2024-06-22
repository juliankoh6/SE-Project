import sys
import sqlite3
from PyQt5 import QtWidgets, uic

# Class for handling functionality and UI of partnered clinics page
class ClinicInfo(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClinicInfo, self).__init__()
        uic.loadUi('Clinics_Info_ui.ui', self)

        # Set up the database connection
        self.db = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.db.cursor()

        # Retrieve clinic data that are approved
        self.cursor.execute(
            "SELECT Clinic_ID, Clinic_Name, Clinic_Speciality, Clinic_Contact_Number, Clinic_Location FROM Clinic "
            "WHERE Clinic_Status = 1")
        clinics = self.cursor.fetchall()

        # Get the QScrollArea and its layout
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, 'scrollArea')

        # Create a widget to hold the clinics
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setObjectName("scrollWidget")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # Populate the layout with clinic data
        for clinic in clinics:
            self.add_clinic(clinic)

        # Connect the button to the redirect_to_login method
        self.commandLinkButton.clicked.connect(self.redirect_to_login)

        # Show the window
        self.show()

    # Add Frames of clinics with their info to the page
    def add_clinic(self, clinic):
        clinic_id, clinic_name, speciality, contact_number, address = clinic

        # Create a frame for each clinic
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # Create a vertical layout for the frame
        vbox = QtWidgets.QVBoxLayout()

        # Add clinic details
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
            doctor_info = "".join(
                f"Name: {doctor[0]}Job: {doctor[1]}Specialty: {doctor[2]}" for doctor in doctors)
            QtWidgets.QMessageBox.information(self, "Doctors Information", f"Doctors for this clinic:{doctor_info}")
        else:
            QtWidgets.QMessageBox.information(self, "No Doctors", "No doctors found for this clinic.")

    #Return to login page
    def redirect_to_login(self):
        from CAD_Login import LoginApp
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ClinicInfo()
    window.show()
    sys.exit(app.exec_())
