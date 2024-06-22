import sys
from PyQt5 import QtWidgets, uic
import sqlite3
from email_sender import send_email


# Class for Admin Dashboard that handles UI and functionality of the page
class Admin_Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super(Admin_Dashboard, self).__init__()
        # Load the UI
        uic.loadUi('Admin_Dashboard_ui.ui', self)

        # Connect to the SQLite database
        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.current_clinic = None
        self.load_pending_clinic()
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
                'Clinic_Specialty': 'Clinic Specialty',
                'Owner_NRIC': 'Owner NRIC',
                'Clinic_Email': 'Clinic Email',
                'Clinic_Location': 'Clinic Location',
                'Clinic_Contact_Number': 'Clinic Contact Number'
            }
            column_indices = {
                'Clinic_Name': 1,
                'Clinic_Specialty': 2,
                'Owner_NRIC': 3,
                'Clinic_Email': 4,
                'Clinic_Location': 5,
                'Clinic_Contact_Number': 6
            }

            # Update the labels with the corresponding clinic information
            for label, col_name in zip(labels, columns.keys()):
                label.setText(f"{columns[col_name]}: {pending_clinic[column_indices[col_name]]}")
        else:
            # clear the labels if no clinics that are pending approval clinics remaining
            self.clear_labels()

    # Function to clear all labels
    def clear_labels(self):
        labels = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
        for label in labels:
            label.setText("")

    # Function to accept a clinic's application
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

            # Load the next pending clinic
            self.load_pending_clinic()
        else:
            QtWidgets.QMessageBox.warning(self, "No Pending Clinics", "There are no more clinics pending approval.")

    # Function to reject a clinic's application
    def reject_clinic(self):
        if self.current_clinic:
            clinic_id = self.current_clinic[0]
            clinic_email = self.current_clinic[4]
            reason = self.Reason.toPlainText().strip()

            # Send rejection email
            subject = "Clinic Application Rejected"
            body = "We regret to inform you that your clinic application has been rejected."
            if reason:
                body += f"Reason: {reason}"
            send_email(clinic_email, subject, body)

            # Delete the clinic from the database
            self.cursor.execute("DELETE FROM Clinic WHERE Clinic_ID = ?", (clinic_id,))
            self.conn.commit()

            # Load the next pending clinic
            self.load_pending_clinic()
        else:
            QtWidgets.QMessageBox.warning(self, "No Pending Clinics", "There are no more clinics pending approval.")

    # Log out
    def redirect_to_login(self):
        from CAD_Login import CallADoctorApp
        self.login_window = CallADoctorApp()
        self.login_window.show()
        self.close()


app = QtWidgets.QApplication(sys.argv)
window = Admin_Dashboard()
window.show()
app.exec_()
