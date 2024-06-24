import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication
from CAD_Login import Admin_Dashboard

@pytest.fixture(scope="module")
def app():
    return QApplication([])

@pytest.fixture
def admin_dashboard(app):
    return Admin_Dashboard()

@patch('CAD_Login.send_email')
@patch('CAD_Login.QMessageBox.warning')
def test_accept_clinic(mock_warning, mock_send_email, admin_dashboard):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    pending_clinic = (1, "Test Clinic", "Test Specialty", "S1234567A", "clinic@example.com", "Test Location", "12345678")
    mock_cursor.fetchone.side_effect = [pending_clinic, None]
    mock_conn.cursor.return_value = mock_cursor

    admin_dashboard.conn = mock_conn
    admin_dashboard.cursor = mock_cursor
    admin_dashboard.load_pending_clinic()

    admin_dashboard.accept_clinic()

    actual_calls = [call.args for call in mock_cursor.execute.call_args_list]
    assert ('SELECT * FROM Clinic WHERE Clinic_Status = 0',) in actual_calls
    assert ('UPDATE Clinic SET Clinic_Status = 1 WHERE Clinic_ID = ?', (1,)) in actual_calls
    assert actual_calls.count(('SELECT * FROM Clinic WHERE Clinic_Status = 0',)) == 2

    mock_conn.commit.assert_called_once()
    mock_send_email.assert_called_once_with("clinic@example.com", "Clinic Application Approved", "Congratulations! Your clinic application has been approved.")
    mock_warning.assert_called_with(admin_dashboard, "Clinic Accepted", "The clinic has been accepted and notified.")

@patch('CAD_Login.send_email')
@patch('CAD_Login.QMessageBox.warning')
def test_reject_clinic(mock_warning, mock_send_email, admin_dashboard):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    pending_clinic = (1, "Test Clinic", "Test Specialty", "S1234567A", "clinic@example.com", "Test Location", "12345678")
    mock_cursor.fetchone.side_effect = [pending_clinic, None]
    mock_conn.cursor.return_value = mock_cursor

    admin_dashboard.conn = mock_conn
    admin_dashboard.cursor = mock_cursor
    admin_dashboard.load_pending_clinic()

    admin_dashboard.Reason = MagicMock()
    admin_dashboard.Reason.toPlainText.return_value = "Incomplete documents"

    admin_dashboard.reject_clinic()

    # Check the calls made to execute
    actual_calls = [call.args for call in mock_cursor.execute.call_args_list]
    assert ('SELECT * FROM Clinic WHERE Clinic_Status = 0',) in actual_calls
    assert ('DELETE FROM Clinic WHERE Clinic_ID = ?', (1,)) in actual_calls
    assert actual_calls.count(('SELECT * FROM Clinic WHERE Clinic_Status = 0',)) == 2

    mock_conn.commit.assert_called_once()
    mock_send_email.assert_called_once_with("clinic@example.com", "Clinic Application Rejected", "We regret to inform you that your clinic application has been rejected. Reason: Incomplete documents")
    mock_warning.assert_called_with(admin_dashboard, "Clinic Rejected", "The clinic has been successfully rejected.")

@patch('CAD_Login.QMessageBox.warning')
def test_load_pending_clinic_with_no_pending(mock_warning, admin_dashboard):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # No pending clinic
    mock_conn.cursor.return_value = mock_cursor

    admin_dashboard.conn = mock_conn
    admin_dashboard.cursor = mock_cursor
    admin_dashboard.load_pending_clinic()

    assert admin_dashboard.current_clinic is None
    for label in [admin_dashboard.label, admin_dashboard.label_2, admin_dashboard.label_3, admin_dashboard.label_4, admin_dashboard.label_5, admin_dashboard.label_6]:
        assert label.text() == ""

@patch('CAD_Login.QMessageBox.warning')
def test_redirect_to_login(mock_warning, admin_dashboard):
    with patch.object(admin_dashboard, 'close') as mock_close:
        with patch('CAD_Login.LoginApp') as mock_login_app:
            admin_dashboard.redirect_to_login()
            mock_close.assert_called_once()
            mock_login_app.assert_called_once()
            mock_login_app().show.assert_called_once()
