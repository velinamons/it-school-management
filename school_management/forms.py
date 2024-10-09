from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from school_management.utils.enums import AgeGroup
from .models import Student, ContactMessage, Experience, Goal, Course, Group


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


class SuggestionForm(forms.Form):
    AGE_GROUP_CHOICES = AgeGroup.choices()
    EXPERIENCE_CHOICES = [
        (exp.name, exp.description) for exp in Experience.objects.all()
    ]
    LEARNING_GOAL_CHOICES = [(goal.name, goal.name) for goal in Goal.objects.all()]

    age_group = forms.ChoiceField(
        label="Age Group:",
        choices=AGE_GROUP_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        error_messages={"required": "Please select an age group."},
    )

    experience = forms.ChoiceField(
        label="Programming / Robotics Experience:",
        choices=EXPERIENCE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "experience-input"}),
        error_messages={"required": "Please select your experience level."},
    )

    learning_goal = forms.MultipleChoiceField(
        label="Learning Goal:",
        choices=LEARNING_GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        error_messages={"required": "Please choose a learning goal."},
    )


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "phone_number", "message", "suggested_course", "suggestion_details"]
        labels = {
            "name": "Your Name:",
            "phone_number": "Contact Phone Number:",
            "message": "Message:",
            "suggested_course": "Suggested Course:",
            "suggestion_details": "Your Suggestion Details:",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(
                attrs={"class": "form-control", "maxlength": "250", "rows": "5"}
            ),
            "suggested_course": forms.TextInput(
                attrs={"class": "form-control", "readonly": True}
            ),
            "suggestion_details": forms.TextInput(
                attrs={"class": "form-control", "readonly": True}
            ),
        }
