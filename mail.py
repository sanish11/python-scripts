import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define email sender and receiver
sender_email = "your_email@example.com"
receiver_email = "recipient@example.com"
password = "your_password"

# Create the email object
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Automated Email from Python Script"

# Email body
body = "Hello! This is an automated email sent using Python."
msg.attach(MIMEText(body, 'plain'))

# Connect to the Gmail SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Login and send email
try:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")
finally:
    server.quit()
