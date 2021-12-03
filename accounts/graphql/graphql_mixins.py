from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.forms import EmployeeRegistrationForm
from jobsapp.graphql.graphql_base import Output

UserModel = get_user_model()


class EmployeeRegisterMixin(Output):
    form = EmployeeRegistrationForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        with transaction.atomic():
            f = cls.form(kwargs)

            if f.is_valid():
                user = f.save()
                return cls(success=True)
            else:
                return cls(success=False, errors=f.errors.get_json_data())
