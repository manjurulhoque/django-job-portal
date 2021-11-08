import graphene
from graphene_django.debug import DjangoDebug

from jobsapp.graphql import queries as jobs_queries


class Query(
    jobs_queries.JobQuery,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
