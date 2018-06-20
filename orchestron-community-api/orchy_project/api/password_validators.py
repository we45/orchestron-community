import string
from django.core.exceptions import ValidationError

class PasswordValidator:
    def validate(self, password, user=None):
        if not any(x.isupper() for x in password):
            raise ValidationError('Password should contain atleast 1 upper case letter')
        if not any(x.isdigit() for x in password):
            raise ValidationError('Password should contain atleast 1 numeric letter')
        if not set(string.punctuation).intersection(password): 
            raise ValidationError('Password should contain atleast 1 special character')
        