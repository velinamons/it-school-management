from django import forms
from school_management.models import ContactMessage


class SuggestionForm(forms.Form):
    AGE_GROUP_CHOICES = [
        ('6-8', '6-8 y.o.'),
        ('9-12', '9-12 y.o.'),
        ('13-15', '13-15 y.o.'),
        ('16-18', '16-18 y.o.')
    ]

    EXPERIENCE_CHOICES = [
        ('Beginner', 'Starting from scratch'),
        ('Learner', 'Know basic concepts'),
        ('Builder', 'Made small projects'),
        ('Inventor', 'Created own projects')
    ]

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
        choices=[
            ('Creative Fun', 'Creative Fun'),
            ('Future Education', 'Future Education'),
            ('Innovation Exploration', 'Innovation Exploration')
        ],
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
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '250', 'rows': '5'}),
            'suggested_course': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'suggestion_details': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
        }
