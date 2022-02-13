from calendar import timegm
from datetime import datetime

import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

from jobs.settings import GRAPHQL_JWT
from jobsapp.graphql import queries as jobs_queries
from accounts.graphql import mutations as auth_mutations
from jobsapp.graphql import mutations as job_mutation
from graphql_jwt.settings import jwt_settings


def jwt_payload(user, context=None):
    username = user.get_username()

    exp = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
    payload = {
        "user_id": user.id,
        "email": user.email,
        # 'exp': datetime.utcnow() + GRAPHQL_JWT['JWT_EXPIRATION_DELTA'],
        "exp": timegm(exp.utctimetuple()),
    }

    if jwt_settings.JWT_ALLOW_REFRESH:
        payload["origIat"] = timegm(datetime.utcnow().utctimetuple())

    if jwt_settings.JWT_AUDIENCE is not None:
        payload["aud"] = jwt_settings.JWT_AUDIENCE

    if jwt_settings.JWT_ISSUER is not None:
        payload["iss"] = jwt_settings.JWT_ISSUER
    return payload


class Query(jobs_queries.JobQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(auth_mutations.AuthMutation, job_mutation.JobMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
