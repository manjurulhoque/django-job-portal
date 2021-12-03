from graphene_django import DjangoObjectType
import graphene
from graphene_django.utils import camelize

from .exceptions import WrongUsage

from jobsapp.models import Job


class JobGQLType(DjangoObjectType):
    class Meta:
        model = Job
        fields = "__all__"


class ExpectedErrorType(graphene.Scalar):
    class Meta:
        description = """
        Errors messages and codes mapped to fields or non fields errors.
        Example:
        {
            field_name: [
                {
                    "message": "error message",
                    "code": "error_code"
                }
            ],
            other_field: [
                {
                    "message": "error message",
                    "code": "error_code"
                }
            ],
            nonFieldErrors: [
                {
                    "message": "error message",
                    "code": "error_code"
                }
            ]
        }
    """

    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        elif isinstance(errors, list):
            return {"nonFieldErrors": errors}
        raise WrongUsage("`errors` must be list or dict!")
