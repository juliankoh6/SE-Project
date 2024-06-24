import sys
from PyQt5.QtWidgets import *
from Request_page import *
from CAD_Login import *
import sqlite3
import pytest


class Patient_dashboard_form(object):
    def __init__(self, patient_id):
        self.patient_id = patient_id

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(929, 732)
        font = QtGui.QFont()
        font.setPointSize(8)
        Form.setFont(font)
        Form.setStyleSheet("")
        Form.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Kenya))

        def test_print(item):
            self.doctor_list.clear()
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()

            sentence = item.text()
            clinic_name = sentence.split('\n')[0]

            cursor.execute('SELECT * FROM Clinic WHERE Clinic_Name = ?', (clinic_name,))
            find_clinic_id = cursor.fetchone()

            clinic_id = find_clinic_id[0]
            cursor.execute('SELECT * FROM Doctor WHERE Clinic_ID = ? AND Doctor_Status = 1 ', (clinic_id,))
            doctor_names = cursor.fetchall()

            for item in doctor_names:
                list_item = QListWidgetItem(
                    '{}\n{}'.format(item[2], item[3]))
                self.doctor_list.addItem(list_item)

            conn.close()

        def filter_by():
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()

            speciality = self.Speciality_comboBox.currentText()
            if speciality == 'Show All':
                self.clinic_listWidget.clear()
                Show_clinic()
            else:
                self.clinic_listWidget.clear()
                cursor.execute("SELECT * FROM Clinic")
                data = cursor.fetchall()

                for item in data:
                    parts = item[2].split(', ')

                    for word in parts:
                        if word == speciality:
                            list_item = QListWidgetItem(
                                '{}\n{}'.format(item[1], item[2]))
                            self.clinic_listWidget.addItem(list_item)
                    else:
                        print(False)
                print(speciality)
            conn.close()

        def search():
            search_name = self.Clinic_Search_lineEdit.text()
            self.clinic_listWidget.clear()
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clinic WhERE Clinic_Status = 1")
            data = cursor.fetchall()

            for item in data:
                print(item[0])
                if search_name in item[1]:
                    print(item[1])
                    list_item = QListWidgetItem(
                        '{}\n{}'.format(item[1], item[2]))
                    self.clinic_listWidget.addItem(list_item)
                else:
                    print("false")
            print(search_name)
            conn.close()

        def show_number():
            sentence2 = self.clinic_listWidget.currentItem().text()
            clinic_name = sentence2.split('\n')[0]
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clinic WHERE Clinic_Name = ?", (clinic_name,))
            data = cursor.fetchone()
            phone_number = data[6]
            self.contact_number_entry.setText(phone_number)
            conn.close()

        def show_email():
            sentence2 = self.clinic_listWidget.currentItem().text()
            clinic_name = sentence2.split('\n')[0]
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clinic WHERE Clinic_Name = ?", (clinic_name,))
            data = cursor.fetchone()
            email = data[4]
            self.contact_email_entry.setText(email)
            conn.close()

        def show_address():
            sentence2 = self.clinic_listWidget.currentItem().text()
            clinic_name = sentence2.split('\n')[0]
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clinic WHERE Clinic_Name = ?", (clinic_name,))
            data = cursor.fetchone()
            address = data[5]
            self.address_entry.setText(address)
            conn.close()

        self.clinic_listWidget = QtWidgets.QListWidget(Form)
        self.clinic_listWidget.setGeometry(QtCore.QRect(435, 10, 481, 711))
        self.clinic_listWidget.setObjectName("clinic_listWidget")
        self.clinic_listWidget.setStyleSheet("QListView::item { height: 100px; }")
        self.clinic_listWidget.itemClicked.connect(test_print)
        self.clinic_listWidget.itemClicked.connect(show_number)
        self.clinic_listWidget.itemClicked.connect(show_email)
        self.clinic_listWidget.itemClicked.connect(show_address)

        def Show_clinic():
            conn = sqlite3.connect('call_a_doctor.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clinic WHERE Clinic_Status = 1")
            data = cursor.fetchall()

            for item in data:
                list_item = QListWidgetItem(
                    '{}\n{}'.format(item[1], item[2]))
                self.clinic_listWidget.addItem(list_item)

            conn.close()

        Show_clinic()

        self.Clinic_Search_lineEdit = QtWidgets.QLineEdit(Form)
        self.Clinic_Search_lineEdit.setGeometry(QtCore.QRect(10, 10, 411, 31))
        self.Clinic_Search_lineEdit.setObjectName("Clinic_Search_lineEdit")
        self.Clinic_Search_lineEdit.setPlaceholderText("Search Clinic Here")

        self.Search_pushButton = QtWidgets.QPushButton(Form)
        self.Search_pushButton.setGeometry(QtCore.QRect(10, 50, 411, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Search_pushButton.setFont(font)
        self.Search_pushButton.setIconSize(QtCore.QSize(20, 20))
        self.Search_pushButton.setObjectName("Search_pushButton")
        self.Search_pushButton.clicked.connect(search)

        self.Speciality_comboBox = QtWidgets.QComboBox(Form)
        self.Speciality_comboBox.setGeometry(QtCore.QRect(10, 120, 411, 31))
        self.Speciality_comboBox.addItem("Show All")
        self.Speciality_comboBox.addItem("Cardiology")
        self.Speciality_comboBox.addItem("Dermatology")
        self.Speciality_comboBox.addItem("Endocrinology")
        self.Speciality_comboBox.addItem("Neurology")
        self.Speciality_comboBox.addItem("Orthopedic Surgery")
        self.Speciality_comboBox.addItem("Pediatrics")
        self.Speciality_comboBox.addItem("Ophthalmology")
        self.Speciality_comboBox.addItem("Psychiatry")
        self.Speciality_comboBox.addItem("Dental")
        self.Speciality_comboBox.addItem("Surgery (General)")
        self.Speciality_comboBox.addItem("Radiology")
        self.Speciality_comboBox.addItem("Obstetrics and Gynecology")
        self.Speciality_comboBox.addItem("Urology")
        self.Speciality_comboBox.setObjectName("Speciality_comboBox")
        self.Speciality_comboBox.currentTextChanged.connect(filter_by)
        print(self.Speciality_comboBox.currentText())

        self.SortSpecialityLabel = QtWidgets.QLabel(Form)
        self.SortSpecialityLabel.setGeometry(QtCore.QRect(10, 90, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SortSpecialityLabel.setFont(font)
        self.SortSpecialityLabel.setObjectName("SortSpecialityLabel")

        self.Contact_number_label = QtWidgets.QLabel(Form)
        self.Contact_number_label.setGeometry(QtCore.QRect(10, 220, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Contact_number_label.setFont(font)
        self.Contact_number_label.setObjectName("Contact_number_label")

        self.contact_number_entry = QtWidgets.QLineEdit(Form)
        self.contact_number_entry.setGeometry(QtCore.QRect(170, 220, 251, 31))
        self.contact_number_entry.setText("")
        self.contact_number_entry.setReadOnly(True)
        self.contact_number_entry.setObjectName("contact_number_entry")

        self.Clinic_Information_Label = QtWidgets.QLabel(Form)
        self.Clinic_Information_Label.setGeometry(QtCore.QRect(20, 170, 411, 41))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(18)
        self.Clinic_Information_Label.setFont(font)
        self.Clinic_Information_Label.setObjectName("SortSpecialityLabel_2")

        self.Contact_email_label = QtWidgets.QLabel(Form)
        self.Contact_email_label.setGeometry(QtCore.QRect(10, 260, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Contact_email_label.setFont(font)
        self.Contact_email_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Contact_email_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.Contact_email_label.setObjectName("Contact_email_label")

        self.contact_email_entry = QtWidgets.QLineEdit(Form)
        self.contact_email_entry.setGeometry(QtCore.QRect(170, 260, 251, 31))
        self.contact_email_entry.setText("")
        self.contact_email_entry.setReadOnly(True)
        self.contact_email_entry.setObjectName("contact_email_entry")

        self.address_label = QtWidgets.QLabel(Form)
        self.address_label.setGeometry(QtCore.QRect(10, 300, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.address_label.setFont(font)
        self.address_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.address_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.address_label.setObjectName("address_label")

        self.address_entry = QtWidgets.QTextEdit(Form)
        self.address_entry.setGeometry(QtCore.QRect(170, 300, 251, 141))
        self.address_entry.setText("")
        self.address_entry.setReadOnly(True)
        self.address_entry.setObjectName("address_entry")
        self.address_entry.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.docto_label = QtWidgets.QLabel(Form)
        self.docto_label.setGeometry(QtCore.QRect(10, 450, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.docto_label.setFont(font)
        self.docto_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.docto_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.docto_label.setObjectName("docto_label")

        self.doctor_list = QtWidgets.QListWidget(Form)
        self.doctor_list.setGeometry(QtCore.QRect(170, 450, 251, 271))
        self.doctor_list.setStyleSheet("QListView::item { height: 50px; }")
        self.doctor_list.setObjectName("doctor_list")
        self.doctor_list.setWordWrap(True)

        self.send_request_button = QtWidgets.QPushButton(Form)
        self.send_request_button.setGeometry(QtCore.QRect(10, 680, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.send_request_button.setFont(font)
        self.send_request_button.setIconSize(QtCore.QSize(20, 20))
        self.send_request_button.setObjectName("send_request_button")
        self.send_request_button.clicked.connect(lambda: self.open_request_page(self.patient_id))

        self.Back_to_Login_button = QtWidgets.QPushButton(Form)
        self.Back_to_Login_button.setGeometry(QtCore.QRect(10, 630, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Back_to_Login_button.setFont(font)
        self.Back_to_Login_button.setIconSize(QtCore.QSize(20, 20))
        self.Back_to_Login_button.setObjectName("Back_to_Login_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def open_request_page(self, patient_id):
        if self.doctor_list.currentRow() == -1:
            self.msg_box_name = QMessageBox()
            self.msg_box_name.setText("You haven't choose doctor name yet.")
            self.msg_box_name.setWindowTitle("Notification")
            self.msg_box_name.show()
        else:
            sentence = self.doctor_list.currentItem().text()
            doctor_name = sentence.split('\n')[0]
            sentence2 = self.clinic_listWidget.currentItem().text()
            clinic_name = sentence2.split('\n')[0]
            self.request_page = Request_Page(doctor_name, clinic_name, patient_id)
            self.request_page.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Search_pushButton.setText(_translate("Form", "Search"))
        self.SortSpecialityLabel.setText(_translate("Form", "Filter By Speciality"))
        self.Contact_number_label.setText(_translate("Form", "Contact Number:"))
        self.Clinic_Information_Label.setText(_translate("Form", "CLINIC INFORMATION"))
        self.Contact_email_label.setText(_translate("Form", "Contact Email:"))
        self.address_label.setText(_translate("Form", "Address:"))
        self.docto_label.setText(_translate("Form", "Doctors:"))
        self.send_request_button.setText(_translate("Form", "Send Request"))
        self.Back_to_Login_button.setText(_translate("Form", "Back to Login"))

class Patient_Dashboard(QtWidgets.QWidget):
    def __init__(self, patient_id):
        super().__init__()
        self.patient_id = patient_id
        self.ui = Patient_dashboard_form(patient_id)
        self.ui.setupUi(self)
        self.load_patient_data()

        def redirect_to_login():
            self.close()
            self.login_window = LoginApp()
            self.login_window.show()

        self.ui.Back_to_Login_button.clicked.connect(redirect_to_login)

    def load_patient_data(self):
        conn = sqlite3.connect('call_a_doctor.db')
        cursor = conn.cursor()
        query = "SELECT * FROM Patient WHERE Patient_ID = ?"
        cursor.execute(query, (self.patient_id,))
        patient_data = cursor.fetchone()

        conn.close()

# automated test functions just ignore this
'''
def test_clinic_information(qtbot):
    # test did the information of clinic show successfully.
    window = Patient_Dashboard(patient_id=3)
    window.show()

    qtbot.wait_until(lambda: window.ui.clinic_listWidget.count() > 0)
    item = window.ui.clinic_listWidget.item(0)
    item2 = window.ui.clinic_listWidget.item(1)

    rect = window.ui.clinic_listWidget.visualItemRect(item)
    rect2 = window.ui.clinic_listWidget.visualItemRect(item2)

    qtbot.mouseClick(window.ui.clinic_listWidget.viewport(), Qt.LeftButton, pos=rect.center())
    qtbot.wait(3000)

    clinic_location1 = window.ui.address_entry.toPlainText()
    clinic_email1 = window.ui.contact_email_entry.text()
    clinic_phone1 = window.ui.contact_number_entry.text()

    qtbot.mouseClick(window.ui.clinic_listWidget.viewport(), Qt.LeftButton, pos=rect2.center())
    qtbot.wait(3000)

    clinic_location2 = window.ui.address_entry.toPlainText()
    clinic_email2 = window.ui.contact_email_entry.text()
    clinic_phone2 = window.ui.contact_number_entry.text()

    assert clinic_location1 == 'eee, eee'
    assert clinic_email1 == 'juliankoh6@gmail.com'
    assert clinic_phone1 == '232332323443'

    assert clinic_location2 == 'rerreer, reerer'
    assert clinic_email2 == '433443@gmail.com'
    assert clinic_phone2 == '0143078906'

    qtbot.wait(5000)
    window.close()

def test_no_doctor_Choosen(qtbot):
    # test if clinic is chosen but doctor not and click on send request button directly.
    window = Patient_Dashboard(patient_id=3)
    window.show()

    qtbot.wait_until(lambda: window.ui.clinic_listWidget.count() > 0)
    item = window.ui.clinic_listWidget.item(0)
    text = item.text()

    rect = window.ui.clinic_listWidget.visualItemRect(item)

    qtbot.mouseClick(window.ui.clinic_listWidget.viewport(), Qt.LeftButton, pos=rect.center())
    qtbot.wait(3000)

    qtbot.mouseClick(window.ui.send_request_button, Qt.LeftButton)
    qtbot.wait(3000)

    message_box = window.ui.msg_box_name.text()

    assert text == 'King of the pond Ding Zhen Clinic\nNeurology, Endocrinology, Orthopedic Surgery'
    assert message_box == "You haven't choose doctor name yet."

    qtbot.wait(5000)

    window.close()


def test_Search_clinic(qtbot):
    # test the search clinic function
    window = Patient_Dashboard(patient_id=3)
    window.show()

    qtbot.wait_until(lambda: window.ui.clinic_listWidget.count() > 0)

    qtbot.keyClicks(window.ui.Clinic_Search_lineEdit, 'Emperor')
    qtbot.wait(3000)

    qtbot.mouseClick(window.ui.Search_pushButton, Qt.LeftButton)
    qtbot.wait(3000)

    qtbot.wait_until(lambda: window.ui.clinic_listWidget.count() > 0)

    clinic_item = window.ui.clinic_listWidget.item(0)
    text = clinic_item.text()

    qtbot.mouseClick(window.ui.clinic_listWidget.viewport(), Qt.LeftButton,
                     pos=window.ui.clinic_listWidget.visualItemRect(clinic_item).center())
    qtbot.wait(3000)

    assert text == 'Emperor of the stars Ezfic Clinic\nNeurology, Orthopedic Surgery, Psychiatry, Radiology'

    qtbot.wait(5000)

    window.close()

def test_sort_speciality(qtbot):
    # test the sorting function.
    window = Patient_Dashboard(patient_id=3)
    window.show()

    qtbot.wait_until(lambda: window.ui.clinic_listWidget.count() > 0)

    qtbot.mouseClick(window.ui.Speciality_comboBox, Qt.LeftButton)
    qtbot.wait(1000)
    qtbot.keyClick(window.ui.Speciality_comboBox, Qt.Key_Down)
    qtbot.wait(1000)
    qtbot.keyClick(window.ui.Speciality_comboBox, Qt.Key_Down)
    qtbot.wait(1000)
    qtbot.keyClick(window.ui.Speciality_comboBox, Qt.Key_Down)
    qtbot.wait(1000)
    qtbot.keyClick(window.ui.Speciality_comboBox, Qt.Key_Down)
    qtbot.wait(1000)
    qtbot.keyClick(window.ui.Speciality_comboBox, Qt.Key_Enter)
    qtbot.wait(1000)

    speciality_text = window.ui.Speciality_comboBox.currentText()
    item = window.ui.clinic_listWidget.item(0)
    text = item.text()

    rect = window.ui.clinic_listWidget.visualItemRect(item)

    qtbot.mouseClick(window.ui.clinic_listWidget.viewport(), Qt.LeftButton, pos=rect.center())
    qtbot.wait(3000)

    assert speciality_text == 'Neurology'
    assert text == 'King of the pond Ding Zhen Clinic\nNeurology, Endocrinology, Orthopedic Surgery'

    qtbot.wait(5000)

    window.close()

def test_send_request(qtbot):
    # test if the request able to send to database.
    window = Patient_Dashboard(2)
    window.show()

    qtbot.wait_until(lambda: window.ui.clinic_listWidget.count() > 0)
    Clinic_item = window.ui.clinic_listWidget.item(0)
    text = Clinic_item.text()

    window.ui.clinic_listWidget.setCurrentItem(Clinic_item)

    qtbot.mouseClick(window.ui.clinic_listWidget.viewport(), Qt.LeftButton,
                     pos=window.ui.clinic_listWidget.visualItemRect(Clinic_item).center())
    qtbot.wait(3000)

    qtbot.wait_until(lambda: window.ui.doctor_list.count() > 0)

    Doctor_item = window.ui.doctor_list.item(1)
    Doctor_Text = Doctor_item.text()
    qtbot.mouseClick(window.ui.doctor_list.viewport(), Qt.LeftButton,
                     pos=window.ui.doctor_list.visualItemRect(Doctor_item).center())
    qtbot.wait(3000)

    qtbot.mouseClick(window.ui.send_request_button, Qt.LeftButton)
    qtbot.wait(3000)

    clinic_text = window.ui.request_page.ui.clinicname_entry.text()
    doctor_name = window.ui.request_page.ui.doctorname_entry.text()

    qtbot.keyClicks(window.ui.request_page.ui.requestreason_edit, 'AAA')
    qtbot.wait(3000)

    request_reason = window.ui.request_page.ui.requestreason_edit.toPlainText()

    qtbot.wait(3000)

    qtbot.addWidget(window.ui.request_page.ui.Request_dateEdit)
    new_datetime = QDateTime(QDate(2024, 7, 16), QTime(14, 30))
    window.ui.request_page.ui.Request_dateEdit.setDateTime(new_datetime)

    qtbot.mouseClick(window.ui.request_page.ui.sendrequest_button, Qt.LeftButton)
    qtbot.wait(3000)

    assert text == 'King of the pond Ding Zhen Clinic\nNeurology, Endocrinology, Orthopedic Surgery'
    assert Doctor_Text == 'Alice Johnson\nCardiologist'
    assert clinic_text == 'King of the pond Ding Zhen Clinic'
    assert doctor_name == 'Alice Johnson'
    assert request_reason == 'AAA'

    conn = sqlite3.connect('call_a_doctor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patient_Request WHERE Patient_ID = ?', (window.patient_id,))
    result = cursor.fetchone()
    conn.close()

    print(window.patient_id)
    print(window.ui.patient_id)

    assert result[1] == 2
    assert result[2] == 1
    assert result[3] == 2
    assert result[4] == 0
    assert result[5] == 'AAA'
    assert result[6] == '2024-07-16'
    assert result[7] == '14:30:00'

    conn.close()

    qtbot.wait(5000)

    window.close()
'''

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Patient_Dashboard(3)
    window.show()
    app.exec_()