from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

gmail_user = os.getenv('GMAIL_EMAIL')
gmail_password = os.getenv('GMAIL_PASS')

def notifyTimeout(msg):
    sendMail('Test timeout during testing', msg)

def notifyCompletion():
    sendMail('Test completed on test system', 'The tests on the benchtest were completed successfully')

def notifyError(msg):
    sendMail('Critical error during test!', msg)

def sendMail(subject, body):
    print(f'Sending email from {gmail_user} with subject {subject} and body {body}')
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:
        print ('Something went wrong...')

    # Import the email modules we'll need
    from email.message import EmailMessage

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(body)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = os.getenv('RECEIVERS')

    # Send the message via our own SMTP server.
    server.send_message(msg)
    server.quit()
