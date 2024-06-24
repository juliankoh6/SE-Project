import pytest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from CAD_Login import LoginApp

# Ensure a QApplication instance is running
@pytest.fixture(scope='module')
def app():
    app = QApplication([])
    yield app
    app.quit()

@patch('CAD_Login.QMessageBox.warning')
@patch('CAD_Login.verify_password', return_value=True)
def test_valid_login(mock_verify_password, mock_warning, app):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "Test User", "hashed_password")
    mock_conn.cursor.return_value = mock_cursor

    login_app = LoginApp()
    login_app.conn = mock_conn
    login_app.cursor = mock_cursor

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = "validUser@example.com"

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = "validPass"

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Patient"

    login_app.login()

    mock_warning.assert_not_called()
    mock_verify_password.assert_called_once_with("validPass", "hashed_password")

@patch('CAD_Login.QMessageBox.warning')
@patch('CAD_Login.verify_password', return_value=False)
def test_invalid_login(mock_verify_password, mock_warning, app):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "Test User", "hashed_password")
    mock_conn.cursor.return_value = mock_cursor

    login_app = LoginApp()
    login_app.conn = mock_conn
    login_app.cursor = mock_cursor

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = "validUser@example.com"

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = "invalidPass"

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Patient"

    login_app.login()

    mock_warning.assert_called_once_with(login_app, "Login Failed", "Invalid email or password")
    mock_verify_password.assert_called_once_with("invalidPass", "hashed_password")

@patch('CAD_Login.QMessageBox.warning')
def test_empty_email(mock_warning, app):
    login_app = LoginApp()

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = ""

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = "somePass"

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Patient"

    login_app.login()

    mock_warning.assert_called_once_with(login_app, "Input Error", "Please enter your email")

@patch('CAD_Login.QMessageBox.warning')
def test_empty_password(mock_warning, app):
    login_app = LoginApp()

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = "someUser@example.com"

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = ""

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Patient"

    login_app.login()

    mock_warning.assert_called_once_with(login_app, "Input Error", "Please enter your password")

@patch('CAD_Login.QMessageBox.warning')
def test_empty_fields(mock_warning, app):
    login_app = LoginApp()

    login_app.Email_line = MagicMock()
    login_app.Email_line.text.return_value = ""

    login_app.Password_line = MagicMock()
    login_app.Password_line.text.return_value = ""

    login_app.UserType = MagicMock()
    login_app.UserType.currentText.return_value = "Patient"

    login_app.login()

    mock_warning.assert_called_once_with(login_app, "Input Error", "Please enter your email and password")


