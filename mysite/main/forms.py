from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

ROLES = (
    ("Teacher",  "Teacher"),
    ("Student",  "Student"),
)

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices= ROLES,widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.set_password('password')
        if commit:
            user.save()
        return user