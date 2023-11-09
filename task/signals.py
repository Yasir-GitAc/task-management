from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from .models import Task, Assignment


def send_task_assignment_email(sender,instance, created, **kwargs):
  print('signal working')
  if created:
    assignment = instance

    user = assignment.user.email
    task = assignment.task.title
    company = assignment.task.company

    subject = 'New task assigned!'
    message = f"{task} from {company} has been assigned to you"

    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [user],
      fail_silently=False,
    )

  if not created:
    assignment = instance

    user = assignment.user.email
    task = assignment.task.title
    company = assignment.task.company

    subject = 'Task Updated!'
    message = f"{task} from {company} has been Updated"

    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [user],
      fail_silently=False,
    )

post_save.connect(send_task_assignment_email, sender=Assignment)

