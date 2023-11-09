from django.db import models
from account.models import User
from company.models import Company
from datetime import datetime, timedelta

def default_datetime():
  return datetime.now() + timedelta(days=7)

class Task(models.Model):
  PRIORITY = [
    ("normal", "Normal"),
    ("low", "Low"),
    ("medium","Medium"),
    ("high","High"),
  ]
  STATUS = [
    ("unstarted","Unstarted"),
    ("ongoing","Ongoing"),
    ("finished","Finished"),
    ("unassigned","Unassigned"),
  ]

  title = models.CharField(max_length=255)
  drescription = models.TextField(max_length=455, blank=True, null=True)
  priority = models.CharField(max_length=6, choices=PRIORITY,default="normal")
  checklist = models.TextField(max_length=1000, blank=True, null=True)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  assignee = models.ManyToManyField(User, through='Assignment', related_name='assigned_tasks')
  status = models.CharField(max_length=10, choices=STATUS, default='unassigned')
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  date_created = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)
  finishing_expected = models.DateTimeField(default=default_datetime)
  finishing_date = models.DateTimeField(blank=True,null=True)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-date_created']


class Assignment(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  assigned_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ("task", "user")

  def __str__(self):
    return f"{self.task} was assigned to {self.user} on {self.assigned_date}"