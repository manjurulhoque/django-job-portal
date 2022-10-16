import graphene

from jobsapp.models import Job

from .exceptions import GraphQLError
from .types import JobGQLType


class JobQuery(graphene.ObjectType):
    jobs = graphene.List(JobGQLType)
    job = graphene.Field(JobGQLType, pk=graphene.Int())

    def resolve_jobs(self, info):
        return Job.objects.all()

    def resolve_job(self, info, pk, **kwargs):
        if pk:
            try:
                return Job.objects.get(pk=pk)
            except Job.DoesNotExist:
                return GraphQLError("Job doesn't exists")
        return None
