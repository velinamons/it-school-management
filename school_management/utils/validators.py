from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r'^\(\d{3}\) \d{3}-\d{2}-\d{2}$',
    message="Phone number must be in the format (XXX) XXX-XX-XX."
)
