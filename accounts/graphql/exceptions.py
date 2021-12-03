from django.utils.translation import gettext as _

from jobsapp.graphql.exceptions import GraphQLError


class UserAlreadyVerified(GraphQLError):
    default_message = _("User already verified.")


class InvalidCredentials(GraphQLError):
    default_message = _("Invalid credentials.")


class UserNotVerified(GraphQLError):
    default_message = _("User is not verified.")


class EmailAlreadyInUse(GraphQLError):
    default_message = _("This email is already in use.")
