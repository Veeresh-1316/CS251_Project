from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,Course,Assignment,AssignmentSubmission

ROLES = (
    ("Teacher",  "Teacher"),
    ("Student",  "Student"),
)

class NewUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields['role'].label = "Role"
        # role = forms.ChoiceField(label="Role", choices= ROLES, widget=forms.RadioSelect, required=True)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['role'].widget.attrs.update(
            {
                'placeholder': 'Choose Role',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['username', 'role', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'First name is required',
                'max_length': ' First Name is too long'
            },
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        # user.role = self.cleaned_data('role')
        if commit:
            user.save()
        return user


# class NewUserForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     role = forms.ChoiceField(choices= ROLES, widget=forms.RadioSelect, required=True)

#     class Meta:
#         model = User
#         fields = ("username", "email", "role", "password1", "password2")

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             account = User.objects.get(username=username)
#         except Exception as e:
#             return username
#         raise forms.ValidationError(f"Username {username} is already rgistered")

#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email'].lower()
#         user.role = self.cleaned_data['role']
#         user.set_password('password1')
#         if commit:
#             user.save()
#         return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username"
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user = authenticate(username=username, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'teacher_name', 'course_description']

    def __init__(self, *args, **kwargs):
        super(CourseCreateForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].label = "Course Name"
        self.fields['teacher_name'].label = "Teacher Name"
        self.fields['course_description'].label = "Description"
        #self.fields['end_date'].label = "End Date"

        self.fields['course_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Course Name',
            }
        )


        self.fields['teacher_name'].widget.attrs.update(
            {
                'placeholder': 'Teacher Name',
            }
        )


        self.fields['course_description'].widget.attrs.update(
            {
                'placeholder': 'Description',
            }
        )

    def is_valid(self):
        valid = super(CourseCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(CourseCreateForm, self).save(commit=False)
        if commit:
            course.save()
        return course


class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'marks', 'duration']

    def __init__(self, *args, **kwargs):
        super(AssignmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Assignment Name"
        self.fields['content'].label = "Content"
        self.fields['marks'].label = "Marks"
        self.fields['duration'].label = "Duration"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Enter A Name',
            }
        )

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Content',
            }
        )

        self.fields['marks'].widget.attrs.update(
            {
                'placeholder': 'Enter Marks',
            }
        )

        self.fields['duration'].widget.attrs.update(
            {
                'placeholder': '3 hour, 2 hour etc ...',
            }
        )

    def is_valid(self):
        valid = super(AssignmentCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        asg = super(AssignmentCreateForm, self).save(commit=False)
        if commit:
            asg.save()
        return asg



class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = [ 'comment', 'file']

    def __init__(self, *args, **kwargs):
        super(AssignmentSubmissionForm, self).__init__(*args, **kwargs)
        
        self.fields['comment'].label = "Comment"
        self.fields['file'].label = "Upload File"

        self.fields['comment'].widget.attrs.update(
            {
                'placeholder': 'Enter Comments  Here',
            }
        )

        self.fields['file'].widget.attrs.update(
            {
                'placeholder': 'Upload Your FILE Here',
            }
        )

    def is_valid(self):
        valid = super(AssignmentSubmissionForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        asg = super(AssignmentSubmissionForm, self).save(commit=False)
        if commit:
            asg.save()
        return asg

class course_register_form(forms.Form):
    course_id = forms.CharField(max_length=6)