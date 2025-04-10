from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + 
            str(timestamp) + 
            str(user.email_verify_token)
        )

account_activation_token = AccountActivationTokenGenerator()

# Get the user model from settings
User = settings.AUTH_USER_MODEL