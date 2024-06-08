import smtplib
from email.message import EmailMessage

# Sends an email to receiver from the applications email
def send_email(receiver_email, subject, body, sender_email='kohjulian150@gmail.com', sender_password='lbon slns xpev edgb'):
    try:
        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        # Connect to the SMTP server using SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as context:
            context.login(sender_email, sender_password)
            context.send_message(em)

        # Print the error message if any exception occurs
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
