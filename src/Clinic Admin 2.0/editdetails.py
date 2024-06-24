import sys
import sqlite3
from PyQt5 import QtWidgets, uic

qtCreatorFile = "Edit_Clinic_Details.ui"
Ui_EditClinicDetails, QtBaseClass = uic.loadUiType(qtCreatorFile)

class EditClinicDetails(QtWidgets.QMainWindow, Ui_EditClinicDetails):
    def __init__(self, clinic_id, parent=None):
        super(EditClinicDetails, self).__init__(parent)
        self.setupUi(self)

        self.conn = sqlite3.connect('call_a_doctor.db')
        self.cursor = self.conn.cursor()

        self.clinic_id = clinic_id
        self.load_clinic_details()

        self.SaveDetailsButton.clicked.connect(self.save_details)
        self.BackButton.clicked.connect(self.back_to_dashboard)

    def load_clinic_details(self):
        try:
            self.cursor.execute("SELECT Clinic_Name, Clinic_Contact_Number, Clinic_Email, Clinic_Location, Clinic_Speciality FROM Clinic WHERE Clinic_ID = ?", (self.clinic_id,))
            clinic = self.cursor.fetchone()

            if clinic:
                self.EditClinicNameInput.setText(clinic[0])
                self.EditContactNumberInput.setText(clinic[1])
                self.EditClinicEmailInput.setText(clinic[2])

                address_parts = clinic[3].split(', ')
                if len(address_parts) > 1:
                    self.EditAddress1Input.setText(address_parts[0])
                    self.EditAddress2Input.setText(", ".join(address_parts[1:]))
                else:
                    self.EditAddress1Input.setText(clinic[3])
                    self.EditAddress2Input.clear()

                specialties = clinic[4].split(', ') if clinic[4] else []
                self.set_specialties(specialties)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def set_specialties(self, specialties):
        checkboxes = {
            'General Practice': self.GeneralPracticeCheckBox,
            'Cardiology': self.CardiologyCheckBox,
            'Dermatology': self.DermatologyCheckBox,
            'Endocrinology': self.EndocrinologyCheckBox,
            'Neurology': self.NeurologyCheckBox,
            'Obstetrics and Gynecology': self.ObstericsandGynecologyCheckBox,
            'Psychiatry': self.PsychiatryCheckBox,
            'Pediatrics': self.PediatricsCheckBox,
            'Orthopedic Surgery': self.OrthopedicSurgeryCheckBox,
            'Radiology': self.RadiologyCheckBox,
            'Urology': self.UrologyCheckBox,
            'Surgery (General)': self.SurgeryCheckBox
        }
        for checkbox in checkboxes.values():
            checkbox.setChecked(False)
        for specialty in specialties:
            if specialty in checkboxes:
                checkboxes[specialty].setChecked(True)

    def get_selected_specialties(self):
        checkboxes = {
            'General Practice': self.GeneralPracticeCheckBox,
            'Cardiology': self.CardiologyCheckBox,
            'Dermatology': self.DermatologyCheckBox,
            'Endocrinology': self.EndocrinologyCheckBox,
            'Neurology': self.NeurologyCheckBox,
            'Obstetrics and Gynecology': self.ObstericsandGynecologyCheckBox,
            'Psychiatry': self.PsychiatryCheckBox,
            'Pediatrics': self.PediatricsCheckBox,
            'Orthopedic Surgery': self.OrthopedicSurgeryCheckBox,
            'Radiology': self.RadiologyCheckBox,
            'Urology': self.UrologyCheckBox,
            'Surgery (General)': self.SurgeryCheckBox
        }
        specialties = [specialty for specialty, checkbox in checkboxes.items() if checkbox.isChecked()]
        return specialties

    def save_details(self):
        try:
            clinic_name = self.EditClinicNameInput.text()
            specialties = sorted(set(self.get_selected_specialties()))
            clinic_specialty = ", ".join(specialties)
            clinic_email = self.EditClinicEmailInput.text()
            clinic_address1 = self.EditAddress1Input.text()
            clinic_address2 = self.EditAddress2Input.text()
            clinic_contact_number = self.EditContactNumberInput.text()

            clinic_address = f"{clinic_address1}, {clinic_address2}".strip(", ")

            self.cursor.execute("""
                UPDATE Clinic 
                SET Clinic_Name = ?, Clinic_Speciality = ?, Clinic_Email = ?, Clinic_Location = ?, Clinic_Contact_Number = ? 
                WHERE Clinic_ID = ?
            """, (clinic_name, clinic_specialty, clinic_email, clinic_address, clinic_contact_number, self.clinic_id))

            self.conn.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Clinic details updated successfully!")
            self.back_to_dashboard()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def back_to_dashboard(self):
        from Clinic_Dashboard import Clinic_Dashboard
        self.clinicDashboardWindow = Clinic_Dashboard(self.clinic_id)
        self.clinicDashboardWindow.show()
        self.close()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clinic_id = 8  # This should be dynamically set based on the logged-in user
    window = EditClinicDetails(clinic_id)
    window.show()
    sys.exit(app.exec_())
