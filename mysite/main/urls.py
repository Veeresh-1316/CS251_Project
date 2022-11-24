
from django.urls import path
from .views import *

app_name = "main"   


urlpatterns = [
    path("", homepage, name="homepage"),

    path("register", RegisterStudentView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_request, name= "logout"),
    path("password_reset", password_reset_request, name="password_reset"),
    path("course_create",CourseCreateView.as_view(),name="course_create"),
    path('<int:id>/course-view/', course_single, name='course-view'),
    
    path('create_assignment/<int:class>/', AssignmentCreateView.as_view(), name='create_assignment'),
    path('submit_assignment/<int:id>/', AssignmentSubmissionView.as_view(), name='submit_assignment'),
    path('view_submissions/', AssignmentSubmissionListView.as_view(), name='view_submissions'),
]