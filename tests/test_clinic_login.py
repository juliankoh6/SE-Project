import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication
from CAD_Login import LoginApp

@pytest.fixture(scope="module")
def app():
    return QApplication([])

@pytest.fixture
def login_app(app):
    return LoginApp()

@patch('CAD_Login.QMessageBox.warning')
@patch('CAD_Login.verify_password', return_value=True)
def test_valid_login_clinic(mock_verify_password, mock_warning, login_app):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "Test Clinic", "hashed_password", 1)  # Clinic already approved
    mock_conn.cursor.return_value = mock_cursor

    login_app.conn = mock_conn
    login_app.cursor = mock_cursor

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = "validClinic@example.com"

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = "validPass"

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Clinic"

    with patch.object(login_app, 'open_clinic_dashboard') as mock_open_dashboard:
        login_app.login()
        mock_open_dashboard.assert_called_once_with(1)
        mock_warning.assert_not_called()

@patch('CAD_Login.QMessageBox.warning')
@patch('CAD_Login.verify_password', return_value=True)
def test_invalid_login_clinic_not_approved(mock_verify_password, mock_warning, login_app):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "Test Clinic", "hashed_password", 0)  # Clinic not approved
    mock_conn.cursor.return_value = mock_cursor

    login_app.conn = mock_conn
    login_app.cursor = mock_cursor

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = "validClinic@example.com"

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = "validPass"

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Clinic"

    login_app.login()
    mock_warning.assert_called_once_with(login_app, "Login Failed", "Your Clinic has not been approved yet")

@patch('CAD_Login.QMessageBox.warning')
def test_invalid_login_clinic_wrong_password(mock_warning, login_app):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "Test Clinic", "hashed_password", 1)  # Clinic approved
    mock_conn.cursor.return_value = mock_cursor

    login_app.conn = mock_conn
    login_app.cursor = mock_cursor

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = "validClinic@example.com"

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = "wrongPass"

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Clinic"

    with patch('CAD_Login.verify_password', return_value=False):
        login_app.login()
        mock_warning.assert_called_once_with(login_app, "Login Failed", "Invalid email or password")

@patch('CAD_Login.QMessageBox.warning')
def test_invalid_login_clinic_nonexistent_email(mock_warning, login_app):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # Email not found
    mock_conn.cursor.return_value = mock_cursor

    login_app.conn = mock_conn
    login_app.cursor = mock_cursor

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = "nonexistent@example.com"

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = "validPass"

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Clinic"

    login_app.login()
    mock_warning.assert_called_once_with(login_app, "Login Failed", "Invalid email or password")

@patch('CAD_Login.QMessageBox.warning')
def test_invalid_login_clinic_empty_fields(mock_warning, login_app):
    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = ""

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = ""

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Clinic"

    login_app.login()
    mock_warning.assert_called_once_with(login_app, "Input Error", "Please enter your email and password")

