import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QMessageBox
from Registration import ClinicRegisterApp
import logging

# Configure logging to show only critical messages
logging.basicConfig(level=logging.CRITICAL)

# Ensure a QApplication instance is running
@pytest.fixture(scope='module')
def app():
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def clinic_register_app(app):
    return ClinicRegisterApp()


@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_empty_fields(mock_warning, clinic_register_app):
    # Set up database connection and cursor
    logging.info("Database connection and cursor initialized successfully")

    clinic_register_app.ClinicNameInput = MagicMock()
    clinic_register_app.ClinicNameInput.text.return_value = ""
    clinic_register_app.addressLine1Input = MagicMock()
    clinic_register_app.addressLine1Input.text.return_value = ""
    clinic_register_app.addressLine2Input = MagicMock()
    clinic_register_app.addressLine2Input.text.return_value = ""
    clinic_register_app.ContactNumberInput = MagicMock()
    clinic_register_app.ContactNumberInput.text.return_value = ""
    clinic_register_app.ClinicEmailInput = MagicMock()
    clinic_register_app.ClinicEmailInput.text.return_value = ""
    clinic_register_app.Owner_NRIC = MagicMock()
    clinic_register_app.Owner_NRIC.text.return_value = ""
    clinic_register_app.PasswordInput = MagicMock()
    clinic_register_app.PasswordInput.text.return_value = ""
    clinic_register_app.PasswordInput2 = MagicMock()
    clinic_register_app.PasswordInput2.text.return_value = ""
    clinic_register_app.SpecialtyList = MagicMock()
    clinic_register_app.SpecialtyList.selectedItems.return_value = []

    clinic_register_app.send_application()

    mock_warning.assert_called_once_with(clinic_register_app, "Application Error",
                                         "All fields must be filled and at least one specialty must be selected!")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_password_mismatch(mock_warning, clinic_register_app):
    clinic_register_app.ClinicNameInput = MagicMock()
    clinic_register_app.ClinicNameInput.text.return_value = "Test Clinic"
    clinic_register_app.addressLine1Input = MagicMock()
    clinic_register_app.addressLine1Input.text.return_value = "Address Line 1"
    clinic_register_app.addressLine2Input = MagicMock()
    clinic_register_app.addressLine2Input.text.return_value = "Address Line 2"
    clinic_register_app.ContactNumberInput = MagicMock()
    clinic_register_app.ContactNumberInput.text.return_value = "1234567890"
    clinic_register_app.ClinicEmailInput = MagicMock()
    clinic_register_app.ClinicEmailInput.text.return_value = "test@example.com"
    clinic_register_app.Owner_NRIC = MagicMock()
    clinic_register_app.Owner_NRIC.text.return_value = "123456789012"
    clinic_register_app.PasswordInput = MagicMock()
    clinic_register_app.PasswordInput.text.return_value = "password123"
    clinic_register_app.PasswordInput2 = MagicMock()
    clinic_register_app.PasswordInput2.text.return_value = "different_password"
    clinic_register_app.SpecialtyList = MagicMock()
    mock_specialty_item = MagicMock()
    mock_specialty_item.text.return_value = "Cardiology"
    clinic_register_app.SpecialtyList.selectedItems.return_value = [mock_specialty_item]

    clinic_register_app.send_application()

    mock_warning.assert_called_once_with(clinic_register_app, "Application Error", "Password and confirm password do not match.")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_invalid_contact_number(mock_warning, clinic_register_app):
    clinic_register_app.ClinicNameInput = MagicMock()
    clinic_register_app.ClinicNameInput.text.return_value = "Test Clinic"
    clinic_register_app.addressLine1Input = MagicMock()
    clinic_register_app.addressLine1Input.text.return_value = "Address Line 1"
    clinic_register_app.addressLine2Input = MagicMock()
    clinic_register_app.addressLine2Input.text.return_value = "Address Line 2"
    clinic_register_app.ContactNumberInput = MagicMock()
    clinic_register_app.ContactNumberInput.text.return_value = "123abc"
    clinic_register_app.ClinicEmailInput = MagicMock()
    clinic_register_app.ClinicEmailInput.text.return_value = "test@example.com"
    clinic_register_app.Owner_NRIC = MagicMock()
    clinic_register_app.Owner_NRIC.text.return_value = "123456789012"
    clinic_register_app.PasswordInput = MagicMock()
    clinic_register_app.PasswordInput.text.return_value = "password123"
    clinic_register_app.PasswordInput2 = MagicMock()
    clinic_register_app.PasswordInput2.text.return_value = "password123"
    clinic_register_app.SpecialtyList = MagicMock()
    mock_specialty_item = MagicMock()
    mock_specialty_item.text.return_value = "Cardiology"
    clinic_register_app.SpecialtyList.selectedItems.return_value = [mock_specialty_item]

    clinic_register_app.send_application()

    mock_warning.assert_called_once_with(clinic_register_app, "Application Error", "Contact number must be at least 10 digits and contain only numbers.")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_invalid_email(mock_warning, clinic_register_app):
    clinic_register_app.ClinicNameInput = MagicMock()
    clinic_register_app.ClinicNameInput.text.return_value = "Test Clinic"
    clinic_register_app.addressLine1Input = MagicMock()
    clinic_register_app.addressLine1Input.text.return_value = "Address Line 1"
    clinic_register_app.addressLine2Input = MagicMock()
    clinic_register_app.addressLine2Input.text.return_value = "Address Line 2"
    clinic_register_app.ContactNumberInput = MagicMock()
    clinic_register_app.ContactNumberInput.text.return_value = "1234567890"
    clinic_register_app.ClinicEmailInput = MagicMock()
    clinic_register_app.ClinicEmailInput.text.return_value = "test@invalid"
    clinic_register_app.Owner_NRIC = MagicMock()
    clinic_register_app.Owner_NRIC.text.return_value = "123456789012"
    clinic_register_app.PasswordInput = MagicMock()
    clinic_register_app.PasswordInput.text.return_value = "password123"
    clinic_register_app.PasswordInput2 = MagicMock()
    clinic_register_app.PasswordInput2.text.return_value = "password123"
    clinic_register_app.SpecialtyList = MagicMock()
    mock_specialty_item = MagicMock()
    mock_specialty_item.text.return_value = "Cardiology"
    clinic_register_app.SpecialtyList.selectedItems.return_value = [mock_specialty_item]

    clinic_register_app.send_application()

    mock_warning.assert_called_once_with(clinic_register_app, "Email Error", "Please enter a valid email address")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_nric_invalid(mock_warning, clinic_register_app):
    clinic_register_app.ClinicNameInput = MagicMock()
    clinic_register_app.ClinicNameInput.text.return_value = "Test Clinic"
    clinic_register_app.addressLine1Input = MagicMock()
    clinic_register_app.addressLine1Input.text.return_value = "Address Line 1"
    clinic_register_app.addressLine2Input = MagicMock()
    clinic_register_app.addressLine2Input.text.return_value = "Address Line 2"
    clinic_register_app.ContactNumberInput = MagicMock()
    clinic_register_app.ContactNumberInput.text.return_value = "1234567890"
    clinic_register_app.ClinicEmailInput = MagicMock()
    clinic_register_app.ClinicEmailInput.text.return_value = "test@example.com"
    clinic_register_app.Owner_NRIC = MagicMock()
    clinic_register_app.Owner_NRIC.text.return_value = "1234"
    clinic_register_app.PasswordInput = MagicMock()
    clinic_register_app.PasswordInput.text.return_value = "password123"
    clinic_register_app.PasswordInput2 = MagicMock()
    clinic_register_app.PasswordInput2.text.return_value = "password123"
    clinic_register_app.SpecialtyList = MagicMock()
    mock_specialty_item = MagicMock()
    mock_specialty_item.text.return_value = "Cardiology"
    clinic_register_app.SpecialtyList.selectedItems.return_value = [mock_specialty_item]

    clinic_register_app.send_application()

    mock_warning.assert_called_once_with(clinic_register_app, "NRIC Error", "NRIC must be 12 digits and contain only numbers.")

@patch('PyQt5.QtWidgets.QMessageBox.warning')
def test_email_already_exists(mock_warning, clinic_register_app, caplog):
    # Mocking the database response
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    clinic_register_app.conn = mock_conn
    clinic_register_app.cursor = mock_cursor
    mock_cursor.fetchone.return_value = (1,)
    # Mocking user input
    clinic_register_app.ClinicNameInput = MagicMock()
    clinic_register_app.ClinicNameInput.text.return_value = "Test Clinic"
    clinic_register_app.addressLine1Input = MagicMock()
    clinic_register_app.addressLine1Input.text.return_value = "Address Line 1"
    clinic_register_app.addressLine2Input = MagicMock()
    clinic_register_app.addressLine2Input.text.return_value = "Address Line 2"
    clinic_register_app.ContactNumberInput = MagicMock()
    clinic_register_app.ContactNumberInput.text.return_value = "1234567890"
    clinic_register_app.ClinicEmailInput = MagicMock()
    clinic_register_app.ClinicEmailInput.text.return_value = "existing@example.com"
    clinic_register_app.Owner_NRIC = MagicMock()
    clinic_register_app.Owner_NRIC.text.return_value = "123456789012"
    clinic_register_app.PasswordInput = MagicMock()
    clinic_register_app.PasswordInput.text.return_value = "password123"
    clinic_register_app.PasswordInput2 = MagicMock()
    clinic_register_app.PasswordInput2.text.return_value = "password123"
    clinic_register_app.SpecialtyList = MagicMock()
    mock_specialty_item = MagicMock()
    mock_specialty_item.text.return_value = "Cardiology"
    clinic_register_app.SpecialtyList.selectedItems.return_value = [mock_specialty_item]

    clinic_register_app.send_application()

    mock_warning.assert_called_once_with(clinic_register_app, "Email Error", "Email already exists")

def test_valid_registration(clinic_register_app, caplog):
    # Mock database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    clinic_register_app.conn = mock_conn
    clinic_register_app.cursor = mock_cursor

    # Mocking user input
    clinic_register_app.ClinicNameInput = MagicMock()
    clinic_register_app.ClinicNameInput.text.return_value = "Test Clinic"
    clinic_register_app.addressLine1Input = MagicMock()
    clinic_register_app.addressLine1Input.text.return_value = "Address Line 1"
    clinic_register_app.addressLine2Input = MagicMock()
    clinic_register_app.addressLine2Input.text.return_value = "Address Line 2"
    clinic_register_app.ContactNumberInput = MagicMock()
    clinic_register_app.ContactNumberInput.text.return_value = "1234567890"
    clinic_register_app.ClinicEmailInput = MagicMock()
    clinic_register_app.ClinicEmailInput.text.return_value = "existing@example.com"
    clinic_register_app.Owner_NRIC = MagicMock()
    clinic_register_app.Owner_NRIC.text.return_value = "123456789012"
    clinic_register_app.PasswordInput = MagicMock()
    clinic_register_app.PasswordInput.text.return_value = "password123"
    clinic_register_app.PasswordInput2 = MagicMock()
    clinic_register_app.PasswordInput2.text.return_value = "password123"
    clinic_register_app.SpecialtyList = MagicMock()
    mock_specialty_item = MagicMock()
    mock_specialty_item.text.return_value = "Cardiology"
    clinic_register_app.SpecialtyList.selectedItems.return_value = [mock_specialty_item]

    # Mock the database response
    mock_cursor.fetchone.return_value = None

@patch('Registration.QMessageBox.warning')
def test_redirect_to_login(mock_warning, clinic_register_app):
    with patch.object(clinic_register_app, 'close') as mock_close:
        with patch('Registration.LoginApp') as mock_login_app:
            clinic_register_app.redirect_to_login()
            mock_close.assert_called_once()
            mock_login_app.assert_called_once()
            mock_login_app().show.assert_called_once()
