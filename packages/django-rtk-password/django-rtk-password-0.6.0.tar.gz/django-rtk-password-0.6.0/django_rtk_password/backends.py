import uuid

from django.contrib.auth import authenticate, get_user_model
from django_rtk.utils import count_errors, get_errors

from django_rtk_password.models import PasswordResetToken


class Backend:
    def request_password_reset(self, errors, email, **kwargs):
        result = dict(password_reset_token="")
        if count_errors(errors):
            return result

        if not get_user_model().objects.filter(email=email).exists():
            get_errors(errors, "email").append("ACCOUNT_UNKNOWN")
            return result

        password_reset_token, _ = PasswordResetToken.objects.get_or_create(email=email)
        result["password_reset_token"] = password_reset_token.token.hex

        return result

    def reset_password(self, errors, password_reset_token, password, **kwargs):
        result = dict(user=None)
        if count_errors(errors):
            return result

        password_reset_token = PasswordResetToken.objects.filter(
            token=uuid.UUID(password_reset_token)
        ).first()

        if not password_reset_token:
            get_errors(errors, "password_reset_token").append("NOT_FOUND")
            return result

        user = result["user"] = (
            get_user_model().objects.filter(email=password_reset_token.email).first()
        )

        if user:
            user.set_password(password)
            user.save()
            password_reset_token.delete()
        else:
            get_errors(errors, "password_reset_token").append("ACCOUNT_UNKNOWN")

        return result

    def change_password(self, errors, email, password, new_password, **kwargs):
        result = dict(user=None)
        if count_errors(errors):
            return result

        user = get_user_model().objects.filter(email=email).first()
        if not user:
            get_errors(errors, "email").append("ACCOUNT_UNKNOWN")
            return result

        username = getattr(user, get_user_model().USERNAME_FIELD)
        is_authenticated = authenticate(username=username, password=password)
        if not is_authenticated:
            get_errors(errors, "password").append("INVALID_CREDENTIALS")
            return result

        user.set_password(new_password)
        user.save()
        return result
