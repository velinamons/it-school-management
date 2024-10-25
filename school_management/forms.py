from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student, Course, Group, Filia


class StudentRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Student
        fields = ["email", "first_name", "last_name", "phone_number", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self) -> None:
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", "Passwords do not match.")

    def save(self, commit: bool = True) -> Student:
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "autofocus": True}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    def confirm_login_allowed(self, user: Any) -> None:
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code="inactive",
            )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description", "age_group", "experience", "goals"]
        labels = {
            "name": "Course Name:",
            "description": "Description:",
            "age_group": "Age Group:",
            "experience": "Experience:",
            "goals": "Goals:",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "age_group": forms.Select(attrs={"class": "form-control"}),
            "experience": forms.CheckboxSelectMultiple(attrs={"class": "form-check-inline"}),
            "goals": forms.CheckboxSelectMultiple(attrs={"class": "form-check-inline"}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "course", "filia", "group_size"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter group name"}),
            "course": forms.Select(attrs={"class": "form-select"}),
            "filia": forms.Select(attrs={"class": "form-select"}),
            "group_size": forms.NumberInput(attrs={"class": "form-control"}),
        }


class EnrollmentForm(forms.Form):
    filia = forms.ModelChoiceField(queryset=Filia.objects.none(), label="Select Filia")

    def __init__(self, *args, course=None, **kwargs):
        super().__init__(*args, **kwargs)
        if course:
            self.fields["filia"].queryset = Filia.objects.filter(groups__course=course).distinct()