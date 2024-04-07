from django.core.exceptions import ValidationError
import re

def validate_category(category):
    error_message = 'Category:  Must be either interest or hobby'

    valid_categories = [
        'interest',
        'hobby',
    ]

    if category in valid_categories:
        return category
    raise ValidationError(error_message, params={'Current Value':category})

def validate_name(name):
    error_message = 'Name: Must be one word'

    # Convert all names to lowercase
    name = name.lower()

    name_pattern = r'^[A-Za-z]*$'

    valid_name = re.match(name_pattern, name)
    if valid_name:
        return name
    return ValidationError(error_message, params={'Current Value':name})