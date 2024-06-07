import sys
from PyQt5.QtWidgets import *
from Request_page import *



class Patient_dashboard_form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(929, 732)
        font = QtGui.QFont()
        font.setPointSize(8)
        Form.setFont(font)
        Form.setStyleSheet("")
        Form.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Kenya))

        def test_print(item):
            if item.text() == 'the king of pond Ding Zhen clinic':
                self.contact_number_entry.setText("114514")
                self.contact_email_entry.setText("114514")
                self.address_entry.setText("114awdwadaw")
                self.doctor_list.clear()
                self.doctor_list.addItem("Dr Snow Leopard")
                self.doctor_list.addItem("Dr Smoke")
                print('Clicked')
                print(item.text())
            else:
                self.contact_number_entry.setText("sdfafwaf")
                self.contact_email_entry.setText("1awdafff")
                self.address_entry.setText("56757757577577")
                self.doctor_list.clear()
                self.doctor_list.addItem("Dr Amagi")
                print('Clicked')
                print(item.text())


        self.clinic_listWidget = QtWidgets.QListWidget(Form)
        self.clinic_listWidget.setGeometry(QtCore.QRect(435, 10, 481, 711))
        self.clinic_listWidget.setObjectName("clinic_listWidget")
        self.clinic_listWidget.setStyleSheet("QListView::item { height: 100px; }")
        self.clinic_listWidget.itemDoubleClicked.connect(test_print)
        self.clinic_listWidget.addItem("the king of pond Ding Zhen clinic")
        self.clinic_listWidget.addItem("the lord of chicken Kun Kun clinic")

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

        self.Speciality_comboBox = QtWidgets.QComboBox(Form)
        self.Speciality_comboBox.setGeometry(QtCore.QRect(10, 120, 411, 31))
        self.Speciality_comboBox.addItem("Select a speciality")
        self.Speciality_comboBox.addItem("Primary Care")
        self.Speciality_comboBox.addItem("Pediatrics")
        self.Speciality_comboBox.addItem("Internal Medicine")
        self.Speciality_comboBox.addItem("Obstetrics and Gynecology")
        self.Speciality_comboBox.addItem("Dermatology")
        self.Speciality_comboBox.addItem("Orthopedics")
        self.Speciality_comboBox.addItem("Cardiology")
        self.Speciality_comboBox.addItem("Ophthalmology")
        self.Speciality_comboBox.addItem("ENT (Ear, Nose, and Throat)")
        self.Speciality_comboBox.addItem("Psychology")
        self.Speciality_comboBox.addItem("Dental")
        self.Speciality_comboBox.addItem("Chiropractic")
        self.Speciality_comboBox.addItem("Physical Therapy")
        self.Speciality_comboBox.addItem("Oncology")
        self.Speciality_comboBox.addItem("Urology")
        self.Speciality_comboBox.addItem("Endocrinology")
        self.Speciality_comboBox.setObjectName("Speciality_comboBox")

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
        self.send_request_button.clicked.connect(self.open_request_page)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def open_request_page(self):
        if self.doctor_list.currentRow() == -1:
            self.msg_box_name = QMessageBox()
            self.msg_box_name.setText("You haven't choose doctor name yet.")
            self.msg_box_name.setWindowTitle("Notification")
            self.msg_box_name.show()
            print("no u")
        else:
            doctor_name = self.doctor_list.currentItem().text()
            clinic_name = self.clinic_listWidget.currentItem().text()
            self.request_page = Request_Page(doctor_name,clinic_name)
            self.request_page.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Search_pushButton.setText(_translate("Form", "Search"))
        self.SortSpecialityLabel.setText(_translate("Form", "Sort By Speciality"))
        self.Contact_number_label.setText(_translate("Form", "Contact Number:"))
        self.Clinic_Information_Label.setText(_translate("Form", "CLINIC INFORMATION"))
        self.Contact_email_label.setText(_translate("Form", "Contact Email:"))
        self.address_label.setText(_translate("Form", "Address:"))
        self.docto_label.setText(_translate("Form", "Doctors:"))
        self.send_request_button.setText(_translate("Form", "Send Request"))


class Patient_Dashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Patient_dashboard_form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Patient_Dashboard()
    window.show()
    app.exec_()