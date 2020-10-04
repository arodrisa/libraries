import smtplib

gmail_user = 'arodrisaai@gmail.com'
gmail_password = '0Mierdas'

sent_from = gmail_user
to = ['patricv13@gmail.com']
subject = 'muhahahaha'
body = 'Que he aprendido a mandar correos desde python'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except:
    print('Something went wrong...')