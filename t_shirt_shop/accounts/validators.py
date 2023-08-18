from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r'^0\d{9}$',
    message="Phone number must start with '0' followed by 9 digits."
)