import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

from jobsapp.graphql import queries as jobs_queries
from accounts.graphql import mutations as auth_mutations


class Query(
    jobs_queries.JobQuery,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(auth_mutations.AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
