from django.core.exceptions import ValidationError

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

    if name.isalpha():
        return name.lower()
    raise ValidationError(error_message, params={'Current Value':name})