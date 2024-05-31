import sys
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QTextEdit, QMessageBox
)

def initialize_db():
    db_path = os.path.abspath('call_a_doctor.db')
    print(f"Database path: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR(50) NOT NULL UNIQUE,
        Password VARCHAR(50) NOT NULL,
        Role TEXT NOT NULL CHECK (Role IN ('Patient', 'Doctor', 'Administrator'))
    );

    CREATE TABLE IF NOT EXISTS Patients (
        PatientID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Name VARCHAR(100),
        Email VARCHAR(100),
        Phone VARCHAR(15),
        Address TEXT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );

    CREATE TABLE IF NOT EXISTS Doctors (
        DoctorID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Name VARCHAR(100),
        Specialty VARCHAR(50),
        Email VARCHAR(100),
        Phone VARCHAR(15),
        ClinicID INTEGER,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (ClinicID) REFERENCES Clinics(ClinicID)
    );

    CREATE TABLE IF NOT EXISTS Clinics (
        ClinicID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(100),
        Location TEXT,
        ContactInfo VARCHAR(100)
    );

    CREATE TABLE IF NOT EXISTS Appointments (
        AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
        PatientID INTEGER,
        DoctorID INTEGER,
        ClinicID INTEGER,
        Date DATE,
        Time TIME,
        Status TEXT NOT NULL CHECK (Status IN ('Pending', 'Approved', 'Rejected')),
        FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
        FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
        FOREIGN KEY (ClinicID) REFERENCES Clinics(ClinicID)
    );

    CREATE TABLE IF NOT EXISTS Administrators (
        AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Name VARCHAR(100),
        Email VARCHAR(100),
        Phone VARCHAR(15),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );

    CREATE TABLE IF NOT EXISTS MedicalRecords (
        RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
        PatientID INTEGER,
        VisitDate DATE,
        DoctorID INTEGER,
        Notes TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
        FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
    );

    CREATE TABLE IF NOT EXISTS Prescriptions (
        PrescriptionID INTEGER PRIMARY KEY AUTOINCREMENT,
        AppointmentID INTEGER,
        Medication VARCHAR(100),
        Dosage VARCHAR(100),
        Instructions TEXT,
        FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID)
    );
    """)

    cursor.executescript("""
    INSERT OR IGNORE INTO Users (Username, Password, Role) VALUES ('doctor1', 'password', 'Doctor');
    INSERT OR IGNORE INTO Users (Username, Password, Role) VALUES ('patient1', 'password', 'Patient');
    INSERT OR IGNORE INTO Users (Username, Password, Role) VALUES ('admin1', 'password', 'Administrator');

    INSERT OR IGNORE INTO Clinics (Name, Location, ContactInfo) VALUES ('Central Clinic', '123 Main St', '123-456-7890');

    INSERT OR IGNORE INTO Doctors (UserID, Name, Specialty, Email, Phone, ClinicID) VALUES (
        (SELECT UserID FROM Users WHERE Username = 'doctor1'), 
        'Dr. Smith', 'Cardiology', 'dr.smith@clinic.com', '123-456-7890', 
        (SELECT ClinicID FROM Clinics WHERE Name = 'Central Clinic')
    );

    INSERT OR IGNORE INTO Patients (UserID, Name, Email, Phone, Address) VALUES (
        (SELECT UserID FROM Users WHERE Username = 'patient1'), 
        'John Doe', 'john.doe@example.com', '123-456-7890', '456 Elm St'
    );

    INSERT OR IGNORE INTO MedicalRecords (PatientID, VisitDate, DoctorID, Notes) VALUES (
        (SELECT PatientID FROM Patients WHERE Name = 'John Doe'), 
        '2024-01-01', 
        (SELECT DoctorID FROM Doctors WHERE Name = 'Dr. Smith'), 
        'Routine checkup'
    );
    """)

    conn.commit()
    conn.close()

class DoctorDashboard(QMainWindow):
    def __init__(self, doctor_id):
        super().__init__()
        self.setWindowTitle("Doctor Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.doctor_id = doctor_id
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Table for patient records
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(5)
        self.records_table.setHorizontalHeaderLabels(["Record ID", "Patient Name", "Visit Date", "Notes", "Prescriptions"])
        main_layout.addWidget(QLabel("Patient Records"))
        main_layout.addWidget(self.records_table)
        
        self.load_records_button = QPushButton("Load Records")
        self.load_records_button.clicked.connect(self.load_records)
        main_layout.addWidget(self.load_records_button)
        
        # Form for generating prescriptions
        form_layout = QFormLayout()
        
        self.appointment_id_input = QLineEdit()
        form_layout.addRow("Appointment ID:", self.appointment_id_input)
        
        self.medication_input = QLineEdit()
        form_layout.addRow("Medication:", self.medication_input)
        
        self.dosage_input = QLineEdit()
        form_layout.addRow("Dosage:", self.dosage_input)
        
        self.instructions_input = QTextEdit()
        form_layout.addRow("Instructions:", self.instructions_input)
        
        self.generate_prescription_button = QPushButton("Generate Prescription")
        self.generate_prescription_button.clicked.connect(self.generate_prescription)
        form_layout.addWidget(self.generate_prescription_button)
        
        main_layout.addLayout(form_layout)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
    def load_records(self):
        conn = sqlite3.connect('call_a_doctor.db')
        cursor = conn.cursor()
        
        query = """
        SELECT mr.RecordID, p.Name, mr.VisitDate, mr.Notes, group_concat(pr.Medication || ' (' || pr.Dosage || '): ' || pr.Instructions, '; ')
        FROM MedicalRecords mr
        JOIN Patients p ON mr.PatientID = p.PatientID
        LEFT JOIN Prescriptions pr ON mr.RecordID = pr.AppointmentID
        WHERE mr.DoctorID = ?
        GROUP BY mr.RecordID, p.Name, mr.VisitDate, mr.Notes
        """
        
        cursor.execute(query, (self.doctor_id,))
        records = cursor.fetchall()
        conn.close()
        
        self.records_table.setRowCount(len(records))
        for row_num, row_data in enumerate(records):
            for col_num, col_data in enumerate(row_data):
                self.records_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
    
    def generate_prescription(self):
        appointment_id = self.appointment_id_input.text()
        medication = self.medication_input.text()
        dosage = self.dosage_input.text()
        instructions = self.instructions_input.toPlainText()
        
        if appointment_id and medication and dosage and instructions:
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()
            
            try:
                print(f"Inserting Prescription: AppointmentID={appointment_id}, Medication={medication}, Dosage={dosage}, Instructions={instructions}")
                cursor.execute(
                    "INSERT INTO Prescriptions (AppointmentID, Medication, Dosage, Instructions) VALUES (?, ?, ?, ?)",
                    (appointment_id, medication, dosage, instructions)
                )
                conn.commit()
                QMessageBox.information(self, "Success", "Prescription generated successfully.")
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.warning(self, "Error", "Failed to generate prescription.")
            finally:
                conn.close()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

if __name__ == "__main__":
    initialize_db()
    
    app = QApplication(sys.argv)
    doctor_id = 1  # Example doctor ID, you can change this as needed
    window = DoctorDashboard(doctor_id)
    window.show()
    sys.exit(app.exec_())


