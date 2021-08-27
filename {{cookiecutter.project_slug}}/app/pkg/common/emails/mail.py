from django.core.mail import EmailMultiAlternatives, get_connection


def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None, attachments=None):

    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(subject, message, from_email,
                                  recipient_list, connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    if attachments:
        if isinstance(attachments, (list, tuple)):
            for file in attachments:
                mail.attach(file.name, file.read())
        else:
            mail.attach(attachments.name, attachments.read())

    return mail.send()
