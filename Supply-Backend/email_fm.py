


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#Creating a test email to be sent 
message = Mail(
    from_email='from_email@example.com',
    to_emails='eherna26@stedwards.edu',
    subject='Test mail',
    html_content='<strong>Work in progress</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
