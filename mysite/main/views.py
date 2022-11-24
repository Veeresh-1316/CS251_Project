from django.shortcuts import  render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.contrib.auth.models import User  
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.generic import CreateView, FormView,ListView
from django.http import HttpResponseRedirect
from .forms import CourseCreateForm ,AssignmentCreateForm, AssignmentSubmissionForm
from .models import Course,Assignment,AssignmentSubmission
from .forms import NewUserForm, UserLoginForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

User = get_user_model()

def homepage(request):
    course = Course.objects.all().values()
    return render(request=request, template_name='main/home.html', context = {'course': course})

class RegisterStudentView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'main/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('main:login')
        else:
            return render(request, 'main/register.html', {'form': form})


# def register_request(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful." )
#             return redirect("main:homepage")
#         messages.error(request, "Unsuccessful registration. Invalid information.")
#     form = NewUserForm()
#     return render (request=request, template_name="main/register.html", context={"register_form":form})

# def login_request(request):
#     if request.method == "POST":
#         print("1\n")
#         form = UserLoginForm(request, data=request.POST)
#         # if form.is_valid():
#         print("2\n")
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             print("3\n")
#             login(request, user)
#             messages.info(request, f"You are now logged in as {username}.")
#             return redirect("main:homepage")
#         else:
#             messages.error(request,"Invalid username or password.")
#         # else:
#         #     messages.error(request,"Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request=request, template_name="main/login.html", context={"login_form":form})

class LoginView(FormView):
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'main/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("main:homepage")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})



class CourseCreateView(CreateView):
    template_name = 'main/course_create.html'
    form_class = CourseCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('main:homepage')

    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('main:login')
        if self.request.user.is_authenticated and self.request.user.role != 'Teacher':
            return reverse_lazy('main:login')
        return super().dispatch(self.request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CourseCreateView, self).form_valid(form)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



#class CourseView(ListView):
#    model = Course
#    template_name = 'main/courses.html'
#    context_object_name = 'course'
#
#    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
#    # @method_decorator(user_is_instructor, user_is_student)
#    def dispatch(self, request, *args, **kwargs):
#        return super().dispatch(self.request, *args, **kwargs)
#
#    def get_queryset(self):
#        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')


def course_single(request, id):
    course = get_object_or_404(Course, id=id)
    assignment=Assignment.objects.all().values()
    return render(request, "main/view_course.html", {'course': course, 'assignment': assignment })


class AssignmentCreateView(CreateView):
    template_name = 'main/create_assignment.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('main:homepage')

    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('main:login')
        if self.request.user.is_authenticated and self.request.user.role != 'Teacher':
            return reverse_lazy('main:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        course = Course.objects.get(pk=self.kwargs['class'])
        form.instance.course_name=course.course_name
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            

class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'main/assignment_submission_list.html'
    context_object_name = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

class AssignmentSubmissionView(CreateView):
    template_name = 'main/submit_assignment.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('main:homepage')

    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('main:login')
        if self.request.user.is_authenticated and self.request.user.role != 'Student':
            return reverse_lazy('main:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        assignment=Assignment.objects.get(id=self.kwargs['id'])
        form.instance.assignment_title = assignment.title
        form.instance.course_name = assignment.course_name
        return super(AssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'main/view_submissions.html'
    context_object_name = 'assignment_submission'
    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        title= self.kwargs['title']
        name = self.kwargs['name']
        return self.model.objects.all().filter(assignment_title=title , course_name=name).order_by('-id')