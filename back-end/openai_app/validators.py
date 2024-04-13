from django.core.exceptions import ValidationError
import re
from lib.logger import warn_logger


def validate_onet_code(onet_code):
    error_message = 'Onet_Code: Must be in this format ##-####.##'

    code_pattern = r'^\d{2}-\d{4}\.\d{2}$'
    valid_code = re.match(code_pattern, onet_code)
    if valid_code:
        return onet_code

    warn_logger.warning(
        f"Occupation: Onet Code validation failed: {onet_code}")
    raise ValidationError(error_message, params={'Current Value': onet_code})
