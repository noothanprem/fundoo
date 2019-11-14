from django.core.mail import send_mail


def send_reminder_mail(subject, message, sender, reciever):
    send_mail(subject,message,sender,[reciever])