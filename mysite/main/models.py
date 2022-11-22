from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import UserManager

ROLES = (
    ("Student", "Student"),
    ("Teacher", "Teacher")
)

class User(AbstractUser):
    role = models.CharField(max_length=30, choices=ROLES, default="Student")

    objects = UserManager()
    
    def __str__(self):
        return self.email

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    # course_image = models.ImageField(upload_to='media')
    teacher_name = models.CharField(max_length=50)
    teacher_details = models.TextField()
    course_description = models.TextField()
    # created_at = models.DateField(default=timezone.now)
    end_date = models.CharField(max_length=20)

    def __str__(self):
        return self.course_name