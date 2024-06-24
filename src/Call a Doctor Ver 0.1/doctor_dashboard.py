import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QFormLayout, QComboBox,
    QTextEdit, QLabel, QWidget, QMessageBox, QPushButton
)
from PyQt5.QtCore import Qt


class DoctorDashboard(QMainWindow):
    def __init__(self, doctor_id, Clinic_id):
        super().__init__()
        self.setWindowTitle("Doctor Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.clinic_id = Clinic_id
        self.doctor_id = doctor_id
        self.doctor_name = self.get_doctor_name()  # Fetch doctor name
        self.initUI()
        self.load_records()  # Automatically load records
        self.load_appointments()  # Automatically load appointments
        self.load_patient_names()  # Load patient names for prescription
        print(doctor_id)
        print(self.doctor_name)

    def get_doctor_name(self):
        conn = sqlite3.connect("call_a_doctor.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Doctor_Name FROM Doctor WHERE Doctor_ID = ?", (self.doctor_id,))
        doctor = cursor.fetchone()
        conn.close()

        if doctor:
            return doctor[0]
        else:
            return "Unknown Doctor"

    def initUI(self):
        main_layout = QVBoxLayout()

        # Welcome Label
        welcome_label = QLabel(f"Welcome Doctor {self.doctor_name}")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(welcome_label)

        # View Records
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(4)
        self.records_table.setHorizontalHeaderLabels(["Record ID", "Patient Name", "Visit Date", "Prescription"])
        main_layout.addWidget(QLabel("Patient Records"))
        main_layout.addWidget(self.records_table)

        # Appointment Management
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(4)
        self.appointments_table.setHorizontalHeaderLabels(["Patient Name", "Request Date", "Request Time", "Contact"])
        main_layout.addWidget(QLabel("Patient Appointments"))
        main_layout.addWidget(self.appointments_table)

        # Form for generating prescriptions
        form_layout = QFormLayout()

        self.patient_name_combobox = QComboBox()
        form_layout.addRow("Patient Name:", self.patient_name_combobox)

        self.prescription_input = QTextEdit()
        form_layout.addRow("Prescription (Medication, Dosage, Instructions):", self.prescription_input)

        self.generate_prescription_button = QPushButton("Generate Prescription")
        self.generate_prescription_button.clicked.connect(self.generate_prescription)
        form_layout.addWidget(self.generate_prescription_button)

        main_layout.addLayout(form_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_records(self):
        conn = sqlite3.connect("call_a_doctor.db")
        cursor = conn.cursor()

        query = """
        SELECT pr.Record_ID, p.Patient_Name, pr.Visit_Date, pr.Prescription
        FROM Patient_Record pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        WHERE pr.Doctor_ID = ?;
        """

        cursor.execute(query, (self.doctor_id,))
        records = cursor.fetchall()
        conn.close()

        self.records_table.setRowCount(len(records))
        for row_num, row_data in enumerate(records):
            for col_num, col_data in enumerate(row_data):
                self.records_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def load_appointments(self):
        conn = sqlite3.connect("call_a_doctor.db")
        cursor = conn.cursor()

        query = """
        SELECT p.Patient_Name, pr.Request_Date, pr.Request_Time, p.Patient_Contact_Number
        FROM Patient_Request pr
        JOIN Patient p ON pr.Patient_ID = p.Patient_ID
        WHERE pr.Doctor_ID = ? AND pr.Request_State = 1
        """

        cursor.execute(query, (self.doctor_id,))
        appointments = cursor.fetchall()
        conn.close()

        self.appointments_table.setRowCount(len(appointments))
        for row_num, row_data in enumerate(appointments):
            for col_num, col_data in enumerate(row_data):
                self.appointments_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def load_patient_names(self):
        conn = sqlite3.connect("call_a_doctor.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Patient_Name FROM Patient")
        patients = cursor.fetchall()
        conn.close()

        self.patient_name_combobox.clear()
        for patient in patients:
            self.patient_name_combobox.addItem(patient[0])

    def generate_prescription(self):
        patient_name = self.patient_name_combobox.currentText()
        prescription = self.prescription_input.toPlainText()

        if not patient_name or not prescription:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        conn = sqlite3.connect("call_a_doctor.db")
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT Patient_ID FROM Patient WHERE Patient_Name = ?', (patient_name,))
            patient = cursor.fetchone()

            if not patient:
                QMessageBox.warning(self, "Error", "No patient found with this name.")
                return

            patient_id = patient[0]

            selected_items = self.appointments_table.selectedItems()
            if selected_items:
                row = selected_items[0].row()
                request_date_item = self.appointments_table.item(row, 1)
                if request_date_item is not None:
                    request_date = request_date_item.text()
                    print(f"Request Date of selected row: {request_date}")
                    print(f"Doctor id of selected row: {self.doctor_id}")
                    print(f"patient ID of selected row: {patient_id}")
                    cursor.execute(
                        'SELECT * FROM Patient_request WHERE Patient_ID = ? AND Doctor_ID = ? AND Request_Date = ? AND Request_State = 1',
                        (patient_id, self.doctor_id, request_date))
                    result = cursor.fetchone()

                    if result:
                        cursor.execute('''
                                             INSERT INTO Patient_Record (Clinic_ID, Patient_ID, Doctor_ID, Visit_Date, Prescription)
                                             VALUES (?, ?, ?, ?, ?)
                                             ''',
                                       (self.clinic_id, patient_id, self.doctor_id, request_date, prescription))

                        conn.commit()
                        QMessageBox.information(self, "Success", "Prescription generated successfully.")
                    else:
                        self.msg_box_name = QMessageBox()
                        self.msg_box_name.setText("This patient did not send any request with this date yet.")
                        self.msg_box_name.setWindowTitle("Notification")
                        self.msg_box_name.show()
            else:
                self.msg_box_name = QMessageBox()
                self.msg_box_name.setText("You haven't choose a patient request date yet.")
                self.msg_box_name.setWindowTitle("Notification")
                self.msg_box_name.show()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()

        self.load_records()  # Refresh the records table
        self.load_appointments()  # Refresh the appointments table


if __name__ == "__main__":
    db_path = "call_a_doctor.db"  # Path to your database file

    app = QApplication(sys.argv)
    doctor_id = 5  # Example doctor ID, you can change this as needed
    window = DoctorDashboard(doctor_id)
    window.show()
    sys.exit(app.exec_())
