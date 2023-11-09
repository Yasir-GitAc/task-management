from django.db import models
from account.models import User

class Company(models.Model):
  name = models.CharField(max_length=255)
  company_logo = models.ImageField(upload_to='company_logo',default= 'company_logo/blog-3.jpg', blank=True, null=True)
  company_email = models.EmailField(max_length=255, unique=True)
  address = models.CharField(max_length=255, blank=True, null=True)
  company_bio = models.TextField(max_length=455, blank=True, null=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_companies')
  members = models.ManyToManyField(User, through='Membership', related_name='company_members')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

class Membership(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  joined_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ("company", "user")

  def __str__(self):
    return f"{self.user} joined {self.company} on {self.joined_date}"


class Notification(models.Model):
  TYPE = [
    ("assignment","assignment"),
    ("addrequest","addrequest"),
    ("requestaccept","requestaccept"),
    ("information","information"),
  ]
  type = models.CharField(max_length=13,choices=TYPE, default="information")
  title = models.CharField(max_length=255)
  subject = models.CharField(max_length=255, blank=True, null=True)
  sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  company_sender = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
  receivers = models.ManyToManyField(User, related_name='notifications', blank=True)
  company_receivers = models.ManyToManyField(Company, related_name='notifications', blank=True)
  seen = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.subject

  class Meta:
    ordering =  ['-created']

