from django import forms
from .models import ContactMessage, Experience, Goal
from django.core.exceptions import ValidationError
from .enums import AgeGroup


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
        fields = ["name", "phone", "message", "suggested_course", "suggestion_details"]
        labels = {
            "name": "Your Name:",
            "phone": "Contact Phone Number:",
            "message": "Message:",
            "suggested_course": "Suggested Course:",
            "suggestion_details": "Your Suggestion Details:",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
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

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone")
        if phone is None:
            raise ValidationError("Phone number is required.")

        if len(phone) != 15:
            raise ValidationError(f"Please enter a valid phone number: {phone}")

        return phone
