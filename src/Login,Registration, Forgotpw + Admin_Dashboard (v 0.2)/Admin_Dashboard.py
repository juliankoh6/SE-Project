import sys
from PyQt5 import QtWidgets, uic
import sqlite3
from email_sender import send_email


# Class that handles UI and functionality of the dashboard
class Admin_Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super(Admin_Dashboard, self).__init__()
        # Load the UI
        uic.loadUi('ui/Admin_Dashboard_ui.ui', self)

        # Connect to the SQLite database
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.current_clinic = None
        self.load_pending_clinic()
        # Connect buttons to their respective functions
        self.Accept_Button.clicked.connect(self.accept_clinic)
        self.Reject_Button.clicked.connect(self.reject_clinic)
        self.Log_out.clicked.connect(self.redirect_to_login)

    # Load the first pending clinic from the database
    def load_pending_clinic(self):
        # Fetch the first clinic with status 0 (pending) from the database
        self.cursor.execute("SELECT * FROM Clinic WHERE Clinic_Status = 0")
        pending_clinic = self.cursor.fetchone()

        if pending_clinic:
            self.current_clinic = pending_clinic
            # Map the labels to the respective columns in the database
            labels = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
            columns = {
                'Clinic_Name': 'Clinic Name',
                'Clinic_Speciality': 'Clinic Specialty',
                'Owner_NRIC': 'Owner NRIC',
                'Clinic_Email': 'Clinic Email',
                'Clinic_Location': 'Clinic Location',
                'Clinic_Contact_Number': 'Clinic Contact Number'
            }
            column_indices = {
                'Clinic_Name': 1,
                'Clinic_Speciality': 2,
                'Owner_NRIC': 3,
                'Clinic_Email': 4,
                'Clinic_Location': 5,
                'Clinic_Contact_Number': 6
            }

            # Update the labels with the corresponding clinic information
            for label, col_name in zip(labels, columns.keys()):
                label.setText(f"{columns[col_name]}: {pending_clinic[column_indices[col_name]]}")
        else:
            # If no pending clinic is found, clear the labels
            self.current_clinic = None
            self.clear_labels()

    # Function to clear all labels if no remaining clinics that are pending approval
    def clear_labels(self):
        labels = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
        for label in labels:
            label.setText("")

    # Function to accept a clinic's application and send an email
    def accept_clinic(self):
        if self.current_clinic:
            clinic_id = self.current_clinic[0]
            clinic_email = self.current_clinic[4]

            # Update the clinic status to approved (1)
            self.cursor.execute("UPDATE Clinic SET Clinic_Status = 1 WHERE Clinic_ID = ?", (clinic_id,))
            self.conn.commit()

            # Send approval email
            subject = "Clinic Application Approved"
            body = "Congratulations! Your clinic application has been approved."
            send_email(clinic_email, subject, body)
            QtWidgets.QMessageBox.warning(self, "Clinic Accepted", "The clinic has been accepted and notified.")
            # Load the next pending clinic
            self.load_pending_clinic()
        else:
            QtWidgets.QMessageBox.warning(self, "No Pending Clinics", "There are no more clinics pending approval.")

    # Reject a clinic's application and send an email
    def reject_clinic(self):
        if self.current_clinic:
            clinic_id = self.current_clinic[0]
            clinic_email = self.current_clinic[4]
            reason = self.Reason.toPlainText().strip()

            # Send rejection email
            subject = "Clinic Application Rejected"
            body = "We regret to inform you that your clinic application has been rejected."
            if reason:
                body += f" Reason: {reason}"
            send_email(clinic_email, subject, body)

            # Delete the clinic from the database
            self.cursor.execute("DELETE FROM Clinic WHERE Clinic_ID = ?", (clinic_id,))
            self.conn.commit()
            QtWidgets.QMessageBox.warning(self, "Clinic Rejected", "The clinic has been successfully rejected.")
            # Load the next pending clinic
            self.load_pending_clinic()
        else:
            QtWidgets.QMessageBox.warning(self, "No Pending Clinics", "There are no more clinics pending approval.")

    # Log out to login page
    def redirect_to_login(self):
        self.close()
        from CAD_Login import LoginApp
        self.login_window = LoginApp()
        self.login_window.show()


# Create and run the application
app = QtWidgets.QApplication(sys.argv)
window = Admin_Dashboard()
window.show()
app.exec_()

