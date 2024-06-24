import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5 import QtCore
from Registration import RegisterAccountApp

# Ensure a QApplication instance is running
@pytest.fixture(scope='module')
def app():
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def register_app(app):
    return RegisterAccountApp()

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_empty_fields(mock_warning, register_app):
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = ""
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = ""
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = ""
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = ""
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = ""
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = ""
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = ""
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = ""
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate.currentDate()
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = ""
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = ""
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = ""

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Input Error", "Please fill in all required fields")


@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_empty_fields(mock_warning, register_app):
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = ""
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = ""
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = ""
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = ""
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = ""
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = ""
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = ""
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = ""
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate.currentDate()
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = ""
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = ""
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = ""

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Input Error", "Please fill in all required fields")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_password_mismatch(mock_warning, register_app):
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = "Test User"
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = "Last Name"
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = "test@example.com"
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = "password123"
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = "different_password"
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = "Address Line 1"
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = "Address Line 2"
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = "Male"
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate(2000, 1, 1)
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = "NRIC"
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = "123456789012"
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = "0123456789"

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Password Error", "Passwords do not match")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_invalid_email(mock_warning, register_app):
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = "Test User"
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = "Last Name"
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = "tes3examplecom"
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = "password123"
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = "different_password"
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = "Address Line 1"
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = "Address Line 2"
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = "Male"
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate(2000, 1, 1)
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = "NRIC"
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = "123456789012"
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = "0123456789"

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Email Error", "Please enter a valid email address")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_invalid_contact_number(mock_warning, register_app):
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = "Test User"
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = "Last Name"
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = "test@example.com"
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = "password123"
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = "different_password"
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = "Address Line 1"
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = "Address Line 2"
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = "Male"
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate(2000, 1, 1)
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = "NRIC"
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = "123456789012"
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = "01aaeeee9"

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Application Error", "Contact number must be at least 10 digits "
                                                    "and contain only numbers.")


@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_invalid_name(mock_warning, register_app):
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = "Test User"
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = "23344"
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = "test@example.com"
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = "password123"
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = "different_password"
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = "Address Line 1"
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = "Address Line 2"
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = "Male"
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate(2000, 1, 1)
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = "NRIC"
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = "123456789012"
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = "01aaeeee9"

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Name Error", "Name should only contain alphabets")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_email_already_exists(mock_warning, register_app):
    # Mocking user input
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = "John"
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = "Doe"
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = "john.doe@example.com"
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = "password"
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = "password"
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = "123 Main St"
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = "Apt 456"
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = "Male"
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate(2000, 1, 1)
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = "NRIC"
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = "123456789012"
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = "1234567890"

    # Mock the database response to simulate email already existing
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    register_app.conn = mock_conn
    register_app.cursor = mock_cursor
    mock_cursor.fetchone.return_value = (1,)  # Simulate that the email already exists

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Email Error", "Email already exists")


@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_invalid_name(mock_warning, register_app):
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = "Test User"
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = "23344"
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = "test@example.com"
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = "password123"
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = "different_password"
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = "Address Line 1"
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = "Address Line 2"
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = "Male"
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = QtCore.QDate(2000, 1, 1)
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = "NRIC"
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = "123456789012"
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = "01aaeeee9"

    register_app.register_account()

    mock_warning.assert_called_once_with(register_app, "Name Error", "Name should only contain alphabets")

def test_valid_registration(register_app, caplog):
    # Mock database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    register_app.conn = mock_conn
    register_app.cursor = mock_cursor

    # Mocking user input
    register_app.NameInput = MagicMock()
    register_app.NameInput.text.return_value = "John"
    register_app.LastNameInput = MagicMock()
    register_app.LastNameInput.text.return_value = "Doe"
    register_app.emailInput = MagicMock()
    register_app.emailInput.text.return_value = "john.doe@example.com"
    register_app.passwordInput = MagicMock()
    register_app.passwordInput.text.return_value = "password"
    register_app.confirmPasswordInput = MagicMock()
    register_app.confirmPasswordInput.text.return_value = "password"
    register_app.addressLine1Input = MagicMock()
    register_app.addressLine1Input.text.return_value = "123 Main St"
    register_app.addressLine2Input = MagicMock()
    register_app.addressLine2Input.text.return_value = "Apt 456"
    register_app.GenderBox = MagicMock()
    register_app.GenderBox.currentText.return_value = "Male"
    register_app.BirthdateEdit = MagicMock()
    register_app.BirthdateEdit.date.return_value = MagicMock()  # mock a QDate object
    register_app.NumberType = MagicMock()
    register_app.NumberType.currentText.return_value = "NRIC"
    register_app.NumberInput = MagicMock()
    register_app.NumberInput.text.return_value = "123456789012"
    register_app.contactNumberInput = MagicMock()
    register_app.contactNumberInput.text.return_value = "1234567890"

    # Mock the database response
    mock_cursor.fetchone.return_value = None

    # Mock QMessageBox.information
    mock_qmessagebox = MagicMock()
    with patch('PyQt5.QtWidgets.QMessageBox.information', mock_qmessagebox):
        # Execute registration
        with patch.object(register_app, 'redirect_to_login') as mock_redirect:
            register_app.register_account()

        # Assertions
        assert mock_cursor.execute.call_count == 2  # Adjust the expected count based on actual behavior

        # Assert QMessageBox.information call
        mock_qmessagebox.assert_called_once_with(register_app, "Registration Successful",
                                                 "You have successfully registered!", QMessageBox.Ok,
                                                 QMessageBox.Ok)






