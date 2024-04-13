from django.core.exceptions import ValidationError
from lib.logger import warn_logger


def validate_category(category):
    error_message = 'Category:  Must be either interest or hobby'

    valid_categories = [
        'interest',
        'hobby',
    ]

    if category in valid_categories:
        return category

    warn_logger.warning(f"Keyword: Category validation failed: {category}")
    raise ValidationError(error_message, params={'Current Value': category})


def validate_name(name):
    error_message = 'Name: Must be one word'

    if name.isalpha():
        return name.lower()

    warn_logger.warning(f"Keyword: Name validation failed: {name}")
    raise ValidationError(error_message, params={'Current Value': name})
