__author__ = 'racktivity'
__tags__ = 'alertandcontactagent', 'sendMail'

import smtplib

def main(q, i, params, tags):
    smtpserver = params['smtpserver']
    smtplogin = params['smtplogin']
    smtppassword = params['smtppassword']

    subject = params['subject']
    body = params['body']
    sender = params['sender']
    to = params['to']

    msg = "To: %s\r\nFrom: %s\r\nSubject: %s\r\n\r\n%s" % (to, sender, subject, body)

    smtp = smtplib.SMTP(smtpserver)
    if smtplogin or smtppassword:
        smtp.login(smtplogin, smtppassword)

    smtp.sendmail(sender, to, msg)
    smtp.quit()

def match(q, i, params, tags):
    return True