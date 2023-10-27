from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserCreationFormCustom(UserCreationForm):
    username = forms.CharField(label="Username", min_length=5, max_length=150)
    email = forms.EmailField(label="E-Mail")
    first_name = forms.CharField(label="First Name", max_length=150)
    last_name = forms.CharField(label="Last Name", max_length=150, required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def is_username_valid(self):
        username = self.cleaned_data["username"].lower()
        new = User.objects.filter(username=username)
        if new.count() > 0:
            raise ValidationError("The given username is taken")
        return username

    def is_email_valid(self):
        email = self.cleaned_data["email"].lower()
        new = User.objects.filter(email=email)
        if new.count() > 0:
            raise ValidationError("The given email is taken")
        return email

    def does_password2_match(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError("Passwords do not match or are empty")

        return pwd2

    def are_names_valid(self):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]

        if not (first_name):
            raise ValidationError("Name fields cannot be empty")

        return first_name, last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        return user
