import graphene
from . import sub_mutations as user_mutations


class AuthMutation(graphene.ObjectType):
    employee_register = user_mutations.EmployeeRegister.Field()
    employer_register = user_mutations.EmployerRegister.Field()
