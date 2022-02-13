from django.utils.translation import gettext as _


class NotAllowedException(Exception):
    def __init__(self, message):
        self.message = message


class GraphQLError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class WrongUsage(GraphQLError):
    """
        Internal exception
    """

    default_message = _("Wrong usage, check your code!.")


class PermissionDeniedError(GraphQLError):
    default_message = (_("You don't have permission to access this resource."),)
