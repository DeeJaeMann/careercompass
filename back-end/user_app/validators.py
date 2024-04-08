from django.core.exceptions import ValidationError
import re
from lib.logger import warn_logger

def validate_email(email):
    error_message = 'Email: Must be correct format user@domain.(com,edu,org,net)'

    email_pattern = r'^[A-Za-z\d]+[\w\.-]*[A-Za-z\d]+@[A-Za-z\d]+[\w\.-]*[A-Za-z\d]+(?:\.[A-Z|a-z]{2,})+$'
    valid_email = re.match(email_pattern, email)
    if valid_email:
        return email
    
    warn_logger.warning(f"User: Email validation failed: {email}")
    raise ValidationError(error_message, params={'Current Value':email})