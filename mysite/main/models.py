from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from django.utils.translation import gettext as _

from .managers import UserManager

ROLES = (
    ("Student", "Student"),
    ("Teacher", "Teacher")
)

class User(AbstractUser):
    role = models.CharField(max_length=30, choices=ROLES, default="Student")
    courses = models.TextField(blank=True)
    objects = UserManager()

    def add_course(self, element):
        self.courses += "," + element if self.courses else element
        return self.courses
    def get_courses(self):
        return self.courses.split(",") if self.courses else None

    def __str__(self):
        return self.email

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_id = models.CharField(max_length=6)
    teacher_name = models.CharField(max_length=50)
    course_description = models.TextField()
    #created_at = models.DateField(default=timezone.now)
    end_date = models.CharField(max_length=20)

    def __str__(self):
        return self.course_name


class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name=models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    marks = models.CharField(max_length=20)
    duration = models.CharField(max_length=100)
    #created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_title = models.TextField(null=True, blank=True)
    course_name = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True,upload_to="media")

    def __str__(self):
        return self.assignment_title