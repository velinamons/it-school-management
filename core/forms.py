from django import forms


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
            ('Career Interests', 'Career Interests')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        error_messages={
            'required': 'Please choose a learning goal.'
        }
    )
