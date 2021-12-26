import graphene
import graphql_jwt
from . import sub_mutations as user_mutations


class AuthMutation(graphene.ObjectType):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    employee_register = user_mutations.EmployeeRegister.Field()
    employer_register = user_mutations.EmployerRegister.Field()
