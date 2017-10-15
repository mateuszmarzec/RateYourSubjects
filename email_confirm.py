def email_confirm(domain1):
    import os
    import sqlite3
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode
    import django
    from Account.tokens import account_activation_token

    # setup env to Django models
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RateYourSubjects.settings")
    django.setup()
    #
    domain = domain1
    from RateApp.models import UserData

    # create connection and cursor to database
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # get last account which doesn't has activations status
    for row in c.execute(
            "SELECT MAX(id) AS ID, login AS USERNAME, email AS EMAIL FROM RateApp_userdata WHERE is_active=0;"):
        new_user_data = row
    conn.close()

    # get user data from database and create UserData object in this case
    new_user_id = new_user_data[0]
    new_user_username = new_user_data[1]
    new_user_email = new_user_data[2]
    user = UserData.objects.get(login=new_user_username)

    # try to send mail

        # set subject
    subject = 'Sign Up Confirmation'
        # set the 'from' address,
    fromaddr = 'help.triplem@gmail.com'
        # set the 'to' addresses,
    toaddrs = new_user_email
        # set domain :

        # creating custom mail view
    plaintext_path = (os.path.abspath('./')+'/templates/email/email.txt')
    html_path = (os.path.abspath('./')+'/templates/email/email.html')

    ctx = {'username': new_user_username, 'domain': domain, 'uid': urlsafe_base64_encode(force_bytes(new_user_id)), 'token': account_activation_token.make_token(user)}

    text_content = render_to_string(plaintext_path, ctx)
    html_content = render_to_string(html_path, ctx)

        # creating message
    msg = EmailMultiAlternatives(subject, text_content, fromaddr, [toaddrs])
    msg.attach_alternative(html_content, "text/html")

        # send message

    msg.send()


    user.delete()

