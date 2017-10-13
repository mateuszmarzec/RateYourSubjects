import smtplib
import sqlite3, subprocess, os
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template import Context

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

for row in c.execute(
        "SELECT MAX(id) AS ID, login AS USERNAME, email AS EMAIL FROM RateApp_userdata WHERE is_active=0;"):
    new_user_data = row
conn.close()

new_user_username = new_user_data[1]
new_user_email = new_user_data[2]
print(new_user_email)

#sub = subprocess.Popen(["python3 -m smtpd -n -c DebuggingServer localhost:588"], shell=True)

try:
    # set subject
    subject = 'Sign Up Confirmation'
    # set the 'from' address,
    fromaddr = 'help.triplem@gmail.com'
    # set the 'to' addresses,
    toaddrs = new_user_email

    # setup the email server,
    #server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.starttls()
    # add my account login name and password,
    #server.login("help.triplem@gmail.com", "triplemhelp")

    # creating custom mail view
    #plaintext = get_template('templates/email/email.txt')
    #html = get_template('email/email.html')

    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'

    #d = Context({'username': new_user_username})

    #text_content = plaintext.render(d)
    #html_content = html.render(d)

    # creating message
    msg = EmailMultiAlternatives(subject, text_content, fromaddr, [toaddrs])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


    # send the email
    #server.sendmail(fromaddr, toaddrs, msg)
    # disconnect from the server
    #server.quit()
except:
    raise EOFError

#sub.kill()
