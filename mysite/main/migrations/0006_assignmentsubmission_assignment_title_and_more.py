# Generated by Django 4.1.3 on 2022-11-23 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_assignmentsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='assignment_title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='course_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]