from smtplib import SMTP
from email.message import EmailMessage


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'sspproject405@gmail.com'
    msg['from'] = user
    password = 'SSP123456'

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()
    print('worked2')


if __name__ == '__main__':
    print('worked')
    email_alert('Hey', 'Hello world', '87188040@m1.com.sg')
