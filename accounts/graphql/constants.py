from django.utils.translation import gettext as _


class Messages:
    INVALID_PASSWORD = [{"message": _("Invalid password."), "code": "invalid_password"}]
    UNAUTHENTICATED = [{"message": _("Unauthenticated."), "code": "unauthenticated"}]
    INVALID_TOKEN = [{"message": _("Invalid token."), "code": "invalid_token"}]
    EXPIRED_TOKEN = [{"message": _("Expired token."), "code": "expired_token"}]
    ALREADY_VERIFIED = [{"message": _("Account already verified."), "code": "already_verified"}]
    EMAIL_FAIL = [{"message": _("Failed to send email."), "code": "email_fail"}]
    INVALID_CREDENTIALS = [{"message": _("Please, enter valid credentials."), "code": "invalid_credentials"}]
    NOT_VERIFIED = [{"message": _("Please verify your account."), "code": "not_verified"}]
    NOT_VERIFIED_PASSWORD_RESET = [
        {"message": _("Verify your account. A new verification email was sent."), "code": "not_verified"}
    ]
    EMAIL_IN_USE = [{"message": _("A user with that email already exists."), "code": "unique"}]
    USERNAME_NOT_FOUND = [{"message": _("No user with given username found."), "code": "invalid_username"}]
    DATABASE_ERROR = [{"message": _("Internal server error."), "code": "internal_server_error"}]
    PERMISSION_DENIED_ERROR = [{"message": None, "code": "permission_denied"}]
