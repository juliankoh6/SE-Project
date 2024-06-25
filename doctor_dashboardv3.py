import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QFormLayout, QLineEdit,
    QTextEdit, QLabel, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt


class DoctorDashboard(QMainWindow):
    def __init__(self, doctor_id, doctor_name, db_path):
        super().__init__()
        self.setWindowTitle("Doctor Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.db_path = db_path
        self.initUI()

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
        self.appointments_table.setColumnCount(3)
        self.appointments_table.setHorizontalHeaderLabels(["Patient Name", "Visit Date", "Contact"])
        main_layout.addWidget(QLabel("Patient Appointments"))
        main_layout.addWidget(self.appointments_table)

        # Form for generating prescriptions
        form_layout = QFormLayout()

        self.patient_name_input = QLineEdit()
        form_layout.addRow("Patient Name:", self.patient_name_input)

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
        conn = sqlite3.connect("call_a_doctor(v4).db")
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
        conn = sqlite3.connect("call_a_doctor(v4).db")
        cursor = conn.cursor()

        query = """
                SELECT p.Patient_Name, pr.Visit_Date, p.Patient_Contact_Number
                FROM Patient_Record pr
                JOIN Patient p ON pr.Patient_ID = p.Patient_ID
                WHERE pr.Doctor_ID = ?
                """

        cursor.execute(query, (self.doctor_id,))
        appointments = cursor.fetchall()
        conn.close()

        self.appointments_table.setRowCount(len(appointments))
        for row_num, row_data in enumerate(appointments):
            for col_num, col_data in enumerate(row_data):
                self.appointments_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def generate_prescription(self):
        patient_name = self.patient_name_input.text()
        prescription = self.prescription_input.toPlainText()

        if not patient_name or not prescription:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        conn = sqlite3.connect("call_a_doctor(v4).db")
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT Patient_ID FROM Patient WHERE Patient_Name = ?', (patient_name,))
            patient = cursor.fetchone()

            if not patient:
                QMessageBox.warning(self, "Error", "No patient found with this name.")
                return

            patient_id = patient[0]
            clinic_id = 3  # Placeholder, you should use the actual clinic ID
            visit_date = '2024-05-28'  # Placeholder, should be dynamic

            cursor.execute('''
                INSERT INTO Patient_Record (Clinic_ID, Patient_ID, Doctor_ID, Visit_Date, Prescription)
                VALUES (?, ?, ?, ?, ?)
            ''', (clinic_id, patient_id, self.doctor_id, visit_date, prescription))

            conn.commit()
            QMessageBox.information(self, "Success", "Prescription generated successfully.")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()

        self.load_records()
        self.load_appointments()# Refresh the records table


if __name__ == "__main__":
    db_path = "D:\BCSCUN\SEM4\software engineering\Doctor dashboard\call_a_doctor(v4).db"  # Path to your database file

    app = QApplication(sys.argv)
    doctor_id = 2  # Example doctor ID, you can change this as needed
    doctor_name = 'Doctor1'  # Example doctor name, you can change this as needed
    window = DoctorDashboard(doctor_id, doctor_name, db_path)
    window.show()
    sys.exit(app.exec_())