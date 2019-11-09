from django.core.mail import EmailMultiAlternatives
from pyee import BaseEventEmitter
from fundooproject.settings import EMAIL_HOST_USER

ee=BaseEventEmitter()

@ee.on('send_mail')
def send_mail(recipient_email,mail_message):
    subject = 'hello'
    from_email=EMAIL_HOST_USER
    to=recipient_email
    text_content = 'This is an important message.'
    html_content = mail_message
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()