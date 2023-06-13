from django.core.mail import EmailMessage


class Util:

    @staticmethod
    def send_mail(attrs):
        sub = attrs['email_subject']
        body = attrs['email_body']
        to = attrs['to']
        email = EmailMessage(subject=sub, body=body, to=[to])
        email.send()
