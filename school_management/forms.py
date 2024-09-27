from django import forms
from school_management.models import ContactMessage, Course, Experience, Goal
from django.core.exceptions import ValidationError


class SuggestionForm(forms.Form):
    AGE_GROUP_CHOICES = Course.AGE_GROUP_CHOICES
    EXPERIENCE_CHOICES = [(exp.name, exp.description) for exp in Experience.objects.all()]
    LEARNING_GOAL_CHOICES = [(goal.name, goal.name) for goal in Goal.objects.all()]

    age_group = forms.ChoiceField(
        label="Age Group:",
        choices=AGE_GROUP_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        error_messages={
            'required': 'Please select an age group.'
        }
    )

    experience = forms.ChoiceField(
        label="Programming / Robotics Experience:",
        choices=EXPERIENCE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'experience-input'}),
        error_messages={
            'required': 'Please select your experience level.'
        }
    )

    learning_goal = forms.MultipleChoiceField(
        label="Learning Goal:",
        choices=LEARNING_GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        error_messages={
            'required': 'Please choose a learning goal.'
        }
    )


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message', 'suggested_course', 'suggestion_details']
        labels = {
            'name': 'Your Name:',
            'phone': 'Contact Phone Number:',
            'message': 'Message:',
            'suggested_course': 'Suggested Course:',
            'suggestion_details': 'Your Suggestion Details:',  # Custom label
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(0__) ___-__-__'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '250', 'rows': '5'}),
            'suggested_course': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'suggestion_details': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Please enter a valid phone number.")
        return f"+38{phone}"
