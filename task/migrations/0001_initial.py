# Generated by Django 4.2.7 on 2023-11-04 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import task.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0004_alter_membership_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('drescription', models.TextField(blank=True, max_length=455, null=True)),
                ('priority', models.CharField(choices=[('normal', 'Normal'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='normal', max_length=6)),
                ('checklist', models.TextField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[('unstarted', 'Unstarted'), ('ongoing', 'Ongoing'), ('finished', 'Finished'), ('unassigned', 'Unassigned')], default='unassigned', max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('finishing_expected', models.DateTimeField(default=task.models.default_datetime)),
                ('finishing_date', models.DateTimeField(blank=True, null=True)),
                ('assignee', models.ManyToManyField(related_name='assigned_tasks', through='task.Assignment', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together={('task', 'user')},
        ),
    ]
