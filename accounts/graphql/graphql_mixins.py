from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.forms import EmployeeRegistrationForm, EmployerRegistrationForm
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
                user = f.save(commit=False)
                password = f.cleaned_data.get("password1")
                user.set_password(password)
                user.save()
                return cls(success=True)
            else:
                return cls(success=False, errors=f.errors.get_json_data())


class EmployerRegisterMixin(Output):
    form = EmployerRegistrationForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        with transaction.atomic():
            first_name = kwargs.pop("company_name")
            last_name = kwargs.pop("company_address")
            kwargs.update(first_name=first_name, last_name=last_name)
            f = cls.form(kwargs)

            if f.is_valid():
                user = f.save()
                user = f.save(commit=False)
                password = f.cleaned_data.get("password1")
                user.set_password(password)
                user.save()
                return cls(success=True)
            else:
                return cls(success=False, errors=f.errors.get_json_data())
