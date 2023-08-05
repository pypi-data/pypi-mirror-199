import re

from PyInquirer import (ValidationError, Validator)


class LinkedInValidator(Validator):
    pattern = r"^(http(s)?:\/\/)?([\w]+\.)?linkedin\.com\/(pub|in|profile)"

    def validate(self, email):
        if len(email.text):
            if re.match(self.pattern, email.text):
                return True
            else:
                raise ValidationError(
                    message="Invalid LinkedIn Link",
                    cursor_position=len(email.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(email.text))
