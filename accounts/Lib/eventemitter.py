from django.core.mail import EmailMultiAlternatives
from pyee import BaseEventEmitter
from fundooproject.settings import EMAIL_HOST_USER

ee=BaseEventEmitter()

@ee.on('send_mail')
def send_mail(recipient_email,mail_message):
    msg = EmailMultiAlternatives(subject="password reset link", from_email=EMAIL_HOST_USER,
                                 to=[recipient_email], body=mail_message)
    msg.attach_alternative(mail_message, "text/html")
    msg.send()