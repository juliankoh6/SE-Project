from Patient_Dashboard import *

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

    window.ui.msg_box_name.close()

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
    # test if the patient request able to send to database.
    window = Patient_Dashboard(4)
    window.show()

    qtbot.wait_until(lambda: window.ui.clinic_listWidget.count() > 0)

    qtbot.wait(1000)
    Clinic_item = window.ui.clinic_listWidget.item(0)
    text = Clinic_item.text()

    window.ui.clinic_listWidget.setCurrentItem(Clinic_item)

    qtbot.mouseClick(window.ui.clinic_listWidget.viewport(), Qt.LeftButton,
                     pos=window.ui.clinic_listWidget.visualItemRect(Clinic_item).center())
    qtbot.wait(1000)

    qtbot.wait_until(lambda: window.ui.doctor_list.count() > 0)

    Doctor_item = window.ui.doctor_list.item(1)
    Doctor_Text = Doctor_item.text()
    qtbot.mouseClick(window.ui.doctor_list.viewport(), Qt.LeftButton,
                     pos=window.ui.doctor_list.visualItemRect(Doctor_item).center())
    qtbot.wait(1000)

    qtbot.mouseClick(window.ui.send_request_button, Qt.LeftButton)
    qtbot.wait(1000)

    clinic_text = window.ui.request_page.ui.clinicname_entry.text()
    doctor_name = window.ui.request_page.ui.doctorname_entry.text()

    qtbot.keyClicks(window.ui.request_page.ui.requestreason_edit, 'AAA')
    qtbot.wait(1000)

    request_reason = window.ui.request_page.ui.requestreason_edit.toPlainText()

    qtbot.wait(1000)

    qtbot.addWidget(window.ui.request_page.ui.Request_dateEdit)
    new_datetime = QDateTime(QDate(2024, 7, 16), QTime(14, 30))
    window.ui.request_page.ui.Request_dateEdit.setDateTime(new_datetime)
    qtbot.wait(1000)

    qtbot.mouseClick(window.ui.request_page.ui.sendrequest_button, Qt.LeftButton)
    qtbot.wait(1000)

    assert text == 'King of the pond Ding Zhen Clinic\nNeurology, Endocrinology, Orthopedic Surgery'
    assert Doctor_Text == 'Alice Johnson\nCardiologist'
    assert clinic_text == 'King of the pond Ding Zhen Clinic'
    assert doctor_name == 'Alice Johnson'
    assert request_reason == 'AAA'

    conn = sqlite3.connect('call_a_doctor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patient_Request WHERE Patient_ID = ? AND Request_Reason = 'AAA'",
                   (window.patient_id,))
    result = cursor.fetchone()
    conn.close()

    print('            ')

    print(window.patient_id)
    print(window.ui.patient_id)

    print('             ')

    print(result[0])
    print(result[1])
    print(result[2])
    print(result[3])
    print(result[4])

    assert result[1] == 4
    assert result[2] == 1
    assert result[3] == 2
    assert result[4] == 0
    assert result[5] == 'AAA'
    assert result[6] == '2024-07-16'
    assert result[7] == '14:30:00'

    conn.close()

    qtbot.wait(5000)

    window.close()
