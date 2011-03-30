import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
  
msg = MIMEMultipart('alternative')
msg['Subject'] = params['subject']
msg['From'] = params['replyto']
msg['To'] = params['to']
msg.attach(MIMEText(params['body'], 'plain'))
server = smtplib.SMTP('relay.aserver.com')
server.sendmail(params['replyto'], params['to'], msg.as_string())
params['result'] = True
    
