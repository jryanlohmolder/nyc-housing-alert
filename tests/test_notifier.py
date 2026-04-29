import pytest
from unittest.mock import patch, MagicMock
from notifier import send_notification

def test_send_notification_sends_email():

    # Fake listing to pass in
    fake_listings = [
        {
            "lotteryName": "Test Apartments",
            "lotteryId": "12345",
            "borough": "Manhattan",
            "neighborhood": "Harlem", 
        }
    ]

    with patch("notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_notification(fake_listings)

        # Assert the right methods were called
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()

def test_email_subject_contains_listing_count():
    fake_listings = [{"lotteryName": "A"}, {"lotteryName": "B"}]

    with patch("notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_notification(fake_listings)

        # Grab the full email string that was passed to sendmail
        call_args = mock_server.sendmail.call_args
        email_string = call_args[0][2]

        assert "NYC Housing Lottery - 2 new listing(s)" in email_string