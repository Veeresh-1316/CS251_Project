from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from django.utils.translation import gettext as _

from .managers import UserManager
from .validators import *

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
        return self.username

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


def autograder_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.course_name, instance.title, filename)

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name=models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    marks = models.CharField(max_length=20)
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)
    file_types = models.CharField(null=False, blank=False, default=".zip", max_length=100)
    autograder = models.FileField(null=True, blank=True, upload_to=autograder_path)

    def __str__(self):
        return self.course_name + ":" + self.title


def submisison_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.course_name, instance.assignment_title, filename)

class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_title = models.TextField(null=True, blank=True)
    course_name = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    file_types = models.CharField(null=True, blank=True, max_length=100)
    file = ContentTypeRestrictedFileField(null=True, blank=True, upload_to=submisison_path, content_types=str(file_types).split(","))
    submitted_at = models.DateTimeField(default=now)

    marks = models.TextField(null=False, blank=False, default='NA')
    feedback = models.TextField(null=False, blank=False, default='Not Yet Graded')
    
    def __str__(self):
        return self.user.username + ":" + self.course_name + ":" + self.assignment_title