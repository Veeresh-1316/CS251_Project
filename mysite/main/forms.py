from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

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

