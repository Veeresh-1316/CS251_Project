# Generated by Django 4.1.3 on 2022-11-23 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacher_details',
        ),
    ]