from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from account.models import User


def send_welcome_email(sender, instance, created, **kwargs):
  if created :
    user = instance

    subject = 'Welcome to Trello Task Manager'
    message = 'We are glad you are here'

    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [user.email],
      fail_silently=False,
    )

post_save.connect(send_welcome_email, sender=User)