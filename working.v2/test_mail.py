import smtplib

gmail_user = 'JediSchoolTeam3@gmail.com'
gmail_password = 'PractoTeam3@JediSchool'

sent_from = gmail_user
to = ['vmkanthi@gmail.com']
subject = 'Welcome to Task Tracker'
email_text = "You are invited to Join Team1\n\n Click on the Link below to Signup and Join the team.\n"
message = 'Subject: {}\n\n{}'.format(subject, email_text)
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.sendmail(sent_from, to, message)
server.close()
print('Email sent!')
